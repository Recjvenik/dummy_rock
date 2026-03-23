from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Module, Section, Concept, UserProgress, QuizQuestion, QuizAttempt
from .serializers import (ModuleListSerializer, ModuleDetailSerializer, SectionSerializer,
                           ConceptSerializer, UserProgressSerializer,
                           QuizQuestionSerializer, QuizSubmitSerializer, QuizAttemptSerializer)

User = get_user_model()


class ModuleListView(generics.ListAPIView):
    """List all published modules"""
    queryset = Module.objects.filter(is_published=True)
    serializer_class = ModuleListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ModuleDetailView(generics.RetrieveAPIView):
    """Get a specific module with all sections"""
    queryset = Module.objects.filter(is_published=True)
    serializer_class = ModuleDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]


class ConceptListView(generics.ListAPIView):
    """List all concepts tags"""
    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserProgressListView(APIView):
    """Get all progress for the current user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = UserProgress.objects.filter(user=request.user).select_related('module', 'section')
        return Response(UserProgressSerializer(progress, many=True).data)


class UserProgressUpdateView(APIView):
    """Update or create progress for a module"""
    permission_classes = [IsAuthenticated]

    def post(self, request, module_slug):
        try:
            module = Module.objects.get(slug=module_slug)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)

        section_id = request.data.get('section_id')
        section = None
        if section_id:
            try:
                section = Section.objects.get(id=section_id, module=module)
            except Section.DoesNotExist:
                pass

        progress, created = UserProgress.objects.get_or_create(
            user=request.user, module=module,
            defaults={'section': section}
        )

        if not created:
            if section:
                progress.section = section
            progress.completed = request.data.get('completed', progress.completed)
            progress.time_spent += request.data.get('time_spent', 0)
            progress.save()

        return Response(UserProgressSerializer(progress).data)


class QuizQuestionsView(APIView):
    """Get quiz questions for a module"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, module_slug):
        try:
            module = Module.objects.get(slug=module_slug)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)

        questions = QuizQuestion.objects.filter(module=module)
        return Response({
            'module': module.title,
            'question_count': questions.count(),
            'questions': QuizQuestionSerializer(questions, many=True).data,
        })


class QuizSubmitView(APIView):
    """Submit quiz answers and get results"""
    permission_classes = [IsAuthenticated]

    def post(self, request, module_slug):
        try:
            module = Module.objects.get(slug=module_slug)
        except Module.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        answers = serializer.validated_data['answers']
        time_taken = serializer.validated_data['time_taken']
        questions = QuizQuestion.objects.filter(module=module)

        correct = 0
        total = questions.count()
        results = {}

        for q in questions:
            user_ans = answers.get(str(q.id), '').lower()
            is_correct = user_ans == q.correct_answer.lower()
            if is_correct:
                correct += 1
            results[str(q.id)] = {
                'correct': is_correct,
                'correct_answer': q.correct_answer,
                'explanation': q.explanation,
            }

        score = (correct / total * 100) if total > 0 else 0

        attempt = QuizAttempt.objects.create(
            user=request.user,
            module=module,
            score=score,
            total_questions=total,
            correct_answers=correct,
            time_taken=time_taken,
            answers_data=results,
        )

        return Response({
            'score': score,
            'correct': correct,
            'total': total,
            'results': results,
            'attempt_id': attempt.id,
        })


class DashboardStatsView(APIView):
    """Dashboard statistics for the current user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_modules = Module.objects.filter(is_published=True).count()
        completed = UserProgress.objects.filter(user=request.user, completed=True).count()
        in_progress = UserProgress.objects.filter(user=request.user, completed=False).count()
        quiz_attempts = QuizAttempt.objects.filter(user=request.user)
        avg_score = (sum(a.score for a in quiz_attempts) / quiz_attempts.count()
                     if quiz_attempts.exists() else 0)

        return Response({
            'total_modules': total_modules,
            'completed_modules': completed,
            'in_progress_modules': in_progress,
            'quiz_attempts': quiz_attempts.count(),
            'avg_quiz_score': round(avg_score, 1),
        })
