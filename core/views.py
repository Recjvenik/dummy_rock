import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.cache import cache
from modules.models import Module, Concept, GlossaryTerm, LearningPath, PracticalExercise


QUICK_LABS = [
    {'url': '/neural-network/', 'icon': '⚡', 'name': 'Neural Network Lab',
     'desc': 'Build & visualize custom networks on canvas', 'color': '#00ff88'},
    {'url': '/rag-visualizer/', 'icon': '🔍', 'name': 'RAG Pipeline',
     'desc': 'Watch retrieval-augmented generation live', 'color': '#4d96ff'},
    {'url': '/agent-visualizer/', 'icon': '🤖', 'name': 'Agent Flow',
     'desc': 'Multi-agent step-by-step execution', 'color': '#ff8c00'},
    {'url': '/llm-params/', 'icon': '🎛️', 'name': 'LLM Params Lab',
     'desc': 'Tune temperature, top-k, top-p live', 'color': '#b15eff'},
    {'url': '/kmeans/', 'icon': '🔵', 'name': 'K-Means Lab',
     'desc': 'Clustering algorithms visualized', 'color': '#00e5ff'},
    {'url': '/decision-tree/', 'icon': '🌳', 'name': 'Decision Tree',
     'desc': 'Classification & splitting logic', 'color': '#00ff88'},
    {'url': '/attention/', 'icon': '👁️', 'name': 'Attention Lab',
     'desc': 'Self-attention mechanism heatmap', 'color': '#ff6bca'},
    {'url': '/logic-gates/', 'icon': '🔌', 'name': 'Logic Gates Lab',
     'desc': 'Digital logic for beginners', 'color': '#4d96ff'},
    {'url': '/data-sorting/', 'icon': '📊', 'name': 'Data Sorting',
     'desc': 'Algorithm visualization', 'color': '#ff8c00'},
    {'url': '/pattern-recognition/', 'icon': '🧩', 'name': 'Pattern Recognition',
     'desc': 'Logical sequence challenges', 'color': '#b15eff'},
    {'url': '/python-editor/', 'icon': '🐍', 'name': 'Python Editor',
     'desc': 'Write & run Python code in your browser', 'color': '#ffd93d'},
    {'url': '/playground/', 'icon': '🧪', 'name': 'AI Playground',
     'desc': 'Full sandbox environment', 'color': '#00e5ff'},
    {'url': '/ai-chat/', 'icon': '💬', 'name': 'AI Assistant',
     'desc': 'Chat with Claude in realtime', 'color': '#ff6bca'},
]

_DAILY_CHALLENGE_POOL = [
    {
        'title': 'Neural Network Basics',
        'description': 'Open the Neural Network Lab, build a 3-layer network, and run a forward pass. Note what happens to the output when you change the number of hidden neurons.',
        'challenge_type': 'lab',
        'xp_reward': 25,
    },
    {
        'title': 'AI Vocabulary Sprint',
        'description': 'Learn 5 new terms from the Glossary — focus on terms you have not seen before. Can you use each in a sentence?',
        'challenge_type': 'glossary',
        'xp_reward': 20,
    },
    {
        'title': 'Decision Tree Explorer',
        'description': 'Open the Decision Tree Lab and classify at least 10 data points. Try changing the max depth and observe how accuracy changes.',
        'challenge_type': 'lab',
        'xp_reward': 30,
    },
    {
        'title': 'K-Means Clustering Challenge',
        'description': 'In the K-Means Lab, set k=3 and k=5. Explain in your mind why the cluster shapes differ — what does inertia mean?',
        'challenge_type': 'lab',
        'xp_reward': 25,
    },
    {
        'title': 'Attention Mechanism Deep Dive',
        'description': 'Open the Attention Lab. Run a query and screenshot the heatmap. Which tokens attend most to each other and why?',
        'challenge_type': 'lab',
        'xp_reward': 30,
    },
    {
        'title': 'LLM Temperature Experiment',
        'description': 'In the LLM Params Lab, test temperature 0.1 vs 0.9 with the same prompt. Notice how creativity vs accuracy trade off.',
        'challenge_type': 'lab',
        'xp_reward': 25,
    },
    {
        'title': 'RAG Pipeline Walk-Through',
        'description': 'Open the RAG Visualizer and step through a full query. Identify the retrieval step, the ranking, and the final generation.',
        'challenge_type': 'lab',
        'xp_reward': 30,
    },
    {
        'title': 'Daily Login Streak',
        'description': 'Simply log in today and complete any one activity — even reading a glossary term counts! Streaks build mastery.',
        'challenge_type': 'streak',
        'xp_reward': 15,
    },
    {
        'title': 'Logic Gates Fundamentals',
        'description': 'In the Logic Gates Lab, build an XOR gate using only AND, OR, and NOT gates. This is the foundation of all computation!',
        'challenge_type': 'lab',
        'xp_reward': 25,
    },
    {
        'title': 'Pattern Recognition Speed Run',
        'description': 'Complete 5 pattern recognition challenges in a row without any mistakes. Focus — patterns are the language of intelligence.',
        'challenge_type': 'lab',
        'xp_reward': 35,
    },
    {
        'title': 'Ask Claude a Hard Question',
        'description': 'Use the AI Chat to ask Claude a question about something you genuinely do not understand. Read the answer carefully.',
        'challenge_type': 'quiz',
        'xp_reward': 20,
    },
    {
        'title': 'Agent Visualizer Mission',
        'description': 'Open the Agent Visualizer and run a multi-step agent task. How many tool calls did it make? What was its reasoning chain?',
        'challenge_type': 'lab',
        'xp_reward': 30,
    },
    {
        'title': 'Code Explorer Challenge',
        'description': 'Use the AI Code Explorer (AI Chat) to ask how the Neural Network Lab is implemented. Read the codebase explanation.',
        'challenge_type': 'quiz',
        'xp_reward': 20,
    },
    {
        'title': 'Data Sorting Showdown',
        'description': 'In the Data Sorting Lab, compare bubble sort vs quicksort on 50 elements. Which is faster and why?',
        'challenge_type': 'lab',
        'xp_reward': 25,
    },
]


def _get_or_create_daily_challenge(today):
    """Return today's DailyChallenge, auto-creating from the rotating pool if needed."""
    try:
        from school.models import DailyChallenge
        day_index = today.timetuple().tm_yday % len(_DAILY_CHALLENGE_POOL)
        template = _DAILY_CHALLENGE_POOL[day_index]
        challenge, _ = DailyChallenge.objects.get_or_create(
            date=today,
            defaults=template,
        )
        return challenge
    except Exception:
        return None


CHAT_SUGGESTIONS = [
    "What is a neural network?",
    "Explain RAG in simple terms",
    "How do agents use tools?",
    "What is temperature in LLMs?",
    "Difference between fine-tuning and RAG?",
    "What is the ReAct pattern?",
]


def home(request):
    grade_filter = request.GET.get('grade', '')
    if grade_filter and grade_filter != 'all':
        modules = Module.objects.filter(is_published=True, grade_level__in=[grade_filter, 'all']).order_by('order')
    else:
        modules = Module.objects.filter(is_published=True).order_by('order')

    concepts = Concept.objects.all()[:40]
    all_modules_count = Module.objects.filter(is_published=True).count()
    concept_count = Concept.objects.count()
    glossary_count = GlossaryTerm.objects.count()
    exercise_count = PracticalExercise.objects.count()
    stats = {
        'modules': all_modules_count or 13,
        'simulations': 25,
        'concepts': concept_count or 55,
        'labs': len(QUICK_LABS),
        'glossary': glossary_count,
        'exercises': exercise_count,
    }

    context = {
        'modules': modules,
        'concepts': concepts,
        'stats': stats,
        'labs': QUICK_LABS,
        'current_grade': grade_filter,
    }

    # Phase 3: personalised dashboard widgets for authenticated users
    if request.user.is_authenticated:
        today = timezone.now().date()

        # 1. Daily Challenge (auto-generate from rotating pool if none set for today)
        try:
            from school.models import DailyChallenge, ChallengeCompletion
            daily_challenge = DailyChallenge.objects.filter(date=today).first()
            if not daily_challenge:
                daily_challenge = _get_or_create_daily_challenge(today)
            challenge_done = (
                ChallengeCompletion.objects.filter(user=request.user, challenge=daily_challenge).exists()
                if daily_challenge else False
            )
        except Exception:
            daily_challenge = challenge_done = None

        # 2. Continue Learning (last accessed incomplete module)
        try:
            from modules.models import UserProgress
            last_progress = UserProgress.objects.filter(
                user=request.user, completed=False
            ).order_by('-last_accessed').first()
        except Exception:
            last_progress = None

        # 3. Streak heatmap data (last 52 weeks of daily_login events)
        try:
            from gamification.models import XPEvent
            streak_dates = list(
                XPEvent.objects.filter(user=request.user, reason='daily_login')
                .values_list('created_at__date', flat=True)
                .distinct()
            )
            streak_data_json = json.dumps([d.isoformat() for d in streak_dates])
        except Exception:
            streak_data_json = '[]'

        # 4. Skills radar (score per module tag)
        try:
            from modules.models import UserProgress as UP
            radar_data = {
                p.module.tag: int(p.score)
                for p in UP.objects.filter(user=request.user).select_related('module')
                if p.module and p.module.tag
            }
            radar_data_json = json.dumps(radar_data)
        except Exception:
            radar_data_json = '{}'

        # 5. Mini leaderboard (top 5 by XP)
        try:
            from gamification.models import UserXP
            top_xp = UserXP.objects.select_related('user').order_by('-total_xp')[:5]
            top_users = [{'user': obj.user, 'xp': obj.total_xp} for obj in top_xp]
        except Exception:
            top_users = []

        # 6. AI tip (cached per user per day — fetched client-side if not in cache)
        ai_tip = cache.get(f'learning_tip_{request.user.pk}_{today}')

        context.update({
            'daily_challenge': daily_challenge,
            'challenge_done': challenge_done,
            'last_progress': last_progress,
            'streak_data_json': streak_data_json,
            'radar_data_json': radar_data_json,
            'top_users': top_users,
            'ai_tip': ai_tip,
        })

    return render(request, 'core/home.html', context)


def module_learn(request, slug):
    module = get_object_or_404(Module, slug=slug, is_published=True)
    sections = module.sections.all().order_by('order')
    all_modules = Module.objects.filter(is_published=True).order_by('order')
    exercises = module.exercises.all().order_by('order')
    glossary_terms = module.glossary_terms.all().order_by('term')
    resources = module.resources.all().order_by('order') if hasattr(module, 'resources') else []

    # Next / prev modules for navigation
    module_list = list(all_modules)
    idx = next((i for i, m in enumerate(module_list) if m.slug == slug), 0)
    prev_module = module_list[idx - 1] if idx > 0 else None
    next_module = module_list[idx + 1] if idx < len(module_list) - 1 else None

    # Parse learning objectives
    objectives = [o.strip() for o in module.learning_objectives.split('\n') if o.strip()] if module.learning_objectives else []

    return render(request, 'core/module_learn.html', {
        'module': module,
        'sections': sections,
        'all_modules': all_modules,
        'prev_module': prev_module,
        'next_module': next_module,
        'exercises': exercises,
        'glossary_terms': glossary_terms,
        'resources': resources,
        'objectives': objectives,
    })


def playground(request):
    labs = [
        {'url': '/neural-network/', 'icon': '⚡', 'name': 'Neural Network Lab',
         'desc': 'Build, visualize, and run forward passes on custom neural networks.', 'color': '#00ff88'},
        {'url': '/rag-visualizer/', 'icon': '🔍', 'name': 'RAG Pipeline Visualizer',
         'desc': 'Step through retrieval-augmented generation with real chunk scoring.', 'color': '#4d96ff'},
        {'url': '/agent-visualizer/', 'icon': '🤖', 'name': 'Agent Flow Visualizer',
         'desc': 'Watch multi-agent systems plan, execute tools, and reflect on tasks.', 'color': '#ff8c00'},
        {'url': '/llm-params/', 'icon': '🎛️', 'name': 'LLM Parameters Lab',
         'desc': 'Tune temperature, top-k, top-p and see instant quality/cost tradeoffs.', 'color': '#b15eff'},
        {'url': '/ai-chat/', 'icon': '💬', 'name': 'AI Assistant (Claude)',
         'desc': 'Chat directly with Claude Opus 4.5 — ask, explore, debug, learn.', 'color': '#ff6bca'},
        {'url': '/learn/ai-playground/', 'icon': '🧪', 'name': 'AI Playground Module',
         'desc': 'Deep dive into the AI Playground module with interactive content.', 'color': '#00e5ff'},
    ]
    return render(request, 'core/playground.html', {'labs_list': labs})


def rag_visualizer(request):
    return render(request, 'core/rag_visualizer.html')


def agent_visualizer(request):
    return render(request, 'core/agent_visualizer.html')


def neural_network_lab(request):
    return render(request, 'core/neural_network_lab.html')


def llm_params_lab(request):
    return render(request, 'core/llm_params_lab.html')


def ai_chat(request):
    topic = request.GET.get('topic', 'default')
    return render(request, 'core/ai_chat.html', {
        'suggested_questions': CHAT_SUGGESTIONS,
        'initial_topic': topic,
    })


def glossary(request):
    search_q = request.GET.get('q', '')
    letter = request.GET.get('letter', '')
    grade = request.GET.get('grade', '')
    category = request.GET.get('category', '')

    terms = GlossaryTerm.objects.all()
    if search_q:
        terms = terms.filter(term__icontains=search_q)
    if letter:
        terms = terms.filter(term__istartswith=letter)
    if grade and grade != 'all':
        terms = terms.filter(grade_level__in=[grade, 'all'])
    if category:
        terms = terms.filter(category=category)

    categories = GlossaryTerm.objects.values_list('category', flat=True).distinct().order_by('category')
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    return render(request, 'core/glossary.html', {
        'terms': terms,
        'search_q': search_q,
        'current_letter': letter,
        'current_grade': grade,
        'current_category': category,
        'categories': [c for c in categories if c],
        'alphabet': alphabet,
    })


def learning_paths(request):
    paths = LearningPath.objects.all().prefetch_related('modules')
    return render(request, 'core/learning_paths.html', {
        'paths': paths,
    })


def concept_explorer(request):
    concepts = Concept.objects.prefetch_related('modules').all()
    modules = Module.objects.filter(is_published=True).order_by('order')

    # Build concept data for the interactive map
    concept_data = []
    for c in concepts:
        module_slugs = list(c.modules.values_list('slug', flat=True))
        concept_data.append({
            'name': c.name,
            'module_count': len(module_slugs),
            'modules': module_slugs,
        })

    return render(request, 'core/concept_explorer.html', {
        'concepts': concepts,
        'modules': modules,
        'concept_data_json': concept_data,
    })


def kmeans_lab(request):
    return render(request, 'core/kmeans_lab.html')


def decision_tree_lab(request):
    return render(request, 'core/decision_tree_lab.html')


def attention_lab(request):
    return render(request, 'core/attention_lab.html')


def leaderboard(request):
    return render(request, 'gamification/leaderboard.html')


def badges(request):
    return render(request, 'gamification/badges.html')


def onboarding(request):
    return render(request, 'core/onboarding.html')


def logic_gates_lab(request):
    return render(request, 'core/logic_gates_lab.html')


def data_sorting_lab(request):
    return render(request, 'core/data_sorting_lab.html')


def pattern_recognition_lab(request):
    return render(request, 'core/pattern_recognition_lab.html')


def practice_zone(request):
    grade = request.GET.get('grade', '')
    difficulty = request.GET.get('difficulty', '')
    exercise_type = request.GET.get('type', '')

    exercises = PracticalExercise.objects.select_related('module').all()
    if grade and grade != 'all':
        exercises = exercises.filter(grade_level__in=[grade, 'all'])
    if difficulty:
        exercises = exercises.filter(difficulty=difficulty)
    if exercise_type:
        exercises = exercises.filter(exercise_type=exercise_type)

    return render(request, 'core/practice_zone.html', {
        'exercises': exercises,
        'current_grade': grade,
        'current_difficulty': difficulty,
        'current_type': exercise_type,
    })


def ui_showcase(request):
    return render(request, 'core/ui_showcase.html')


def python_editor(request):
    return render(request, 'core/python_editor.html')
