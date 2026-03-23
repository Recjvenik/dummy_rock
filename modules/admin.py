from django.contrib import admin
from .models import Module, Section, Concept, UserProgress, QuizQuestion, QuizAttempt


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'difficulty', 'tag', 'is_published']
    list_filter = ['difficulty', 'tag', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['module', 'order', 'title', 'has_visualizer']
    list_filter = ['module', 'has_visualizer']
    ordering = ['module__order', 'order']


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['modules']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'completed', 'score', 'time_spent']
    list_filter = ['completed']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['module', 'question_type', 'question', 'correct_answer', 'difficulty']
    list_filter = ['module', 'difficulty', 'question_type']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'score', 'correct_answers', 'total_questions', 'attempted_at']
    list_filter = ['module']
