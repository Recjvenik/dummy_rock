import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .bedrock import get_bedrock_client, SYSTEM_PROMPTS, estimate_cost
from . import codemunch


class AIChatView(APIView):
    """REST endpoint for non-streaming AI chat (for quick queries)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message', '')
        history = request.data.get('history', [])
        topic = request.data.get('topic', 'default')
        temperature = float(request.data.get('temperature', 0.7))
        max_tokens = int(request.data.get('max_tokens', 512))

        if not message.strip():
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        messages = [{'role': h['role'], 'content': h['content']} for h in history[-6:]]
        messages.append({'role': 'user', 'content': message})

        try:
            client = get_bedrock_client()
            system = SYSTEM_PROMPTS.get(topic, SYSTEM_PROMPTS['default'])
            result = client.chat(messages, system, max_tokens, temperature)
            cost = estimate_cost(result['input_tokens'], result['output_tokens'])

            return Response({
                'text': result['text'],
                'metrics': {
                    'input_tokens': result['input_tokens'],
                    'output_tokens': result['output_tokens'],
                    'cost_usd': cost,
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ExplainConceptView(APIView):
    """Ask AI to explain a specific AI/ML concept"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        concept = request.data.get('concept', '')
        level = request.data.get('level', 'beginner')

        if not concept:
            return Response({'error': 'Concept is required'}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""Explain "{concept}" for a {level} learner. 
Include: 
1. Simple definition (1-2 sentences)
2. Intuitive analogy
3. How it works (brief)
4. Real-world example
5. Key takeaway

Format with clear sections. Be concise but thorough."""

        try:
            client = get_bedrock_client()
            result = client.chat(
                [{'role': 'user', 'content': prompt}],
                SYSTEM_PROMPTS['ai_basics'],
                max_tokens=800,
                temperature=0.5,
            )
            return Response({
                'concept': concept,
                'level': level,
                'explanation': result['text'],
                'tokens': result['output_tokens'],
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class GenerateQuizView(APIView):
    """Generate quiz questions on a topic using AI"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        topic = request.data.get('topic', 'machine learning')
        count = min(int(request.data.get('count', 5)), 10)
        difficulty = request.data.get('difficulty', 'intermediate')

        prompt = f"""Generate {count} multiple-choice quiz questions about "{topic}" at {difficulty} level.

Return ONLY valid JSON array:
[
  {{
    "question": "...",
    "options": {{"a": "...", "b": "...", "c": "...", "d": "..."}},
    "correct": "a",
    "explanation": "..."
  }}
]"""

        try:
            client = get_bedrock_client()
            result = client.chat(
                [{'role': 'user', 'content': prompt}],
                SYSTEM_PROMPTS['default'],
                max_tokens=2000,
                temperature=0.3,
            )
            text = result['text']
            # Extract JSON from response
            match = re.search(r'\[.*\]', text, re.DOTALL)
            questions = json.loads(match.group()) if match else []
            return Response({'topic': topic, 'questions': questions, 'count': len(questions)})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CodeReviewView(APIView):
    """AI-powered code review for ML/AI code"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code', '')
        language = request.data.get('language', 'python')
        context = request.data.get('context', 'ML/AI code')

        if not code:
            return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""Review this {language} {context}:

```{language}
{code}
```

Provide:
1. Summary of what it does
2. Issues or bugs found
3. Best practice suggestions
4. Performance optimizations
5. Improved version (if needed)"""

        try:
            client = get_bedrock_client()
            result = client.chat(
                [{'role': 'user', 'content': prompt}],
                SYSTEM_PROMPTS['default'],
                max_tokens=1500,
                temperature=0.3,
            )
            return Response({'review': result['text'], 'tokens': result['output_tokens']})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CodeExploreView(APIView):
    """
    AI-powered code exploration using jCodeMunch.
    Searches the AI Lab codebase with 80-99% fewer tokens than reading full files,
    then uses Bedrock to explain/answer questions about what's found.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get('query', '').strip()
        mode = request.data.get('mode', 'explain')  # explain | search | symbol
        symbol_id = request.data.get('symbol_id', '')

        if not query and not symbol_id:
            return Response({'error': 'query or symbol_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not codemunch.is_indexed():
            return Response(
                {'error': 'Codebase not indexed yet. POST to /api/ai/index-codebase/ to index first.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            if symbol_id:
                # Fetch and explain a specific symbol
                sym_result = codemunch.get_code_symbol(symbol_id, context_lines=5)
                code_context = codemunch.format_symbol_source_for_ai(sym_result)
                ai_prompt = f"Explain this code from the AI Lab Django project:\n\n{code_context}\n\nProvide:\n1. What it does\n2. Key parameters/arguments\n3. How it's used in the project\n4. Any important details for learners"
            else:
                # Search symbols first, then explain
                sym_results = codemunch.search_code_symbols(query, max_results=6)
                code_context = codemunch.format_symbols_for_ai(sym_results)

                if mode == 'search':
                    # Just return search results without AI explanation
                    return Response({
                        'query': query,
                        'code_context': code_context,
                        'raw_results': sym_results.get('results', []),
                        'meta': sym_results.get('_meta', {}),
                    })

                ai_prompt = f"""A student is asking about: "{query}"

I searched the AI Lab codebase and found these relevant symbols:

{code_context}

Please explain:
1. What these code elements do in simple terms
2. How they relate to the concept of "{query}"
3. How a student could learn from or experiment with this code
4. Any AI/ML concepts demonstrated in this code

Keep the explanation educational and suitable for students learning AI/ML."""

            client = get_bedrock_client()
            result = client.chat(
                [{'role': 'user', 'content': ai_prompt}],
                SYSTEM_PROMPTS['default'],
                max_tokens=1200,
                temperature=0.4,
            )
            cost = estimate_cost(result['input_tokens'], result['output_tokens'])

            return Response({
                'query': query,
                'explanation': result['text'],
                'code_context': code_context,
                'metrics': {
                    'input_tokens': result['input_tokens'],
                    'output_tokens': result['output_tokens'],
                    'cost_usd': cost,
                },
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class IndexCodebaseView(APIView):
    """Trigger jCodeMunch indexing of the AI Lab codebase (admin only)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)
        try:
            result = codemunch.index_project()
            return Response({
                'status': 'indexed',
                'result': result,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Check if codebase is indexed."""
        return Response({'indexed': codemunch.is_indexed()})


class LearningTipsView(APIView):
    """
    POST /api/ai/learning-tips/
    Returns 3 personalized learning suggestions for a student.
    Response cached per user per day using Django's cache framework.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from django.core.cache import cache
        from django.utils import timezone

        user = request.user
        today = timezone.now().date()
        cache_key = f'learning_tip_{user.pk}_{today}'

        cached = cache.get(cache_key)
        if cached:
            return Response({'tip': cached, 'cached': True})

        # Build context from user's progress
        progress_summary = self._build_progress_summary(user)

        prompt = f"""You are an encouraging AI tutor for an Indian high school student learning AI/ML.
The student's progress:
{progress_summary}

Give exactly 3 short, specific, encouraging learning tips for this student today.
Each tip should be 1-2 sentences. Be concrete, actionable, and motivating.
Format: return only the 3 tips as a single paragraph separated by " · " (no numbering, no markdown)."""

        try:
            client = get_bedrock_client()
            result = client.chat(
                [{'role': 'user', 'content': prompt}],
                system='You are a friendly AI tutor who gives concise, encouraging learning tips.',
                max_tokens=200,
                temperature=0.8,
            )
            tip_text = result['text'].strip()
            cache.set(cache_key, tip_text, timeout=86400)  # Cache 24 hours
            return Response({'tip': tip_text, 'cached': False})
        except Exception as e:
            fallback = "Keep exploring — every module you complete builds a stronger foundation. Try the AI Basics module if you haven't yet · Check the glossary daily to expand your vocabulary · Attempt one lab session today for hands-on practice."
            return Response({'tip': fallback, 'cached': False})

    def _build_progress_summary(self, user):
        lines = []
        try:
            from modules.models import UserProgress
            progress_qs = UserProgress.objects.filter(user=user).select_related('module')
            completed = [p for p in progress_qs if p.completed]
            in_progress = [p for p in progress_qs if not p.completed]
            if completed:
                lines.append(f"Completed modules: {', '.join(p.module.title for p in completed[:3])}")
            if in_progress:
                lines.append(f"In progress: {', '.join(p.module.title for p in in_progress[:2])}")
        except Exception:
            pass
        try:
            from gamification.models import UserXP, DailyStreak
            xp_obj = UserXP.objects.filter(user=user).first()
            if xp_obj:
                lines.append(f"XP: {xp_obj.total_xp}, Level: {xp_obj.level}")
            streak_obj = DailyStreak.objects.filter(user=user).first()
            if streak_obj:
                lines.append(f"Current streak: {streak_obj.current_streak} days")
        except Exception:
            pass
        return '\n'.join(lines) if lines else 'New student, no activity yet.'
