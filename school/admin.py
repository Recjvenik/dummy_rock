from django.contrib import admin
from .models import School, Classroom, Assignment, DailyChallenge, ChallengeCompletion


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'board', 'subscription_tier', 'max_students', 'subscription_end', 'is_active']
    list_filter = ['board', 'subscription_tier', 'city']
    search_fields = ['name', 'city', 'contact_email']
    readonly_fields = ['created_at']


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'teacher', 'grade', 'join_code', 'student_count']
    list_filter = ['grade', 'school']
    search_fields = ['name', 'join_code', 'school__name']
    readonly_fields = ['join_code', 'created_at']
    filter_horizontal = ['students']

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'classroom', 'module', 'status', 'due_date', 'completion_count']
    list_filter = ['status', 'classroom__school']
    search_fields = ['title', 'classroom__name']


@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'challenge_type', 'xp_reward']
    list_filter = ['challenge_type']
    search_fields = ['title']
    ordering = ['-date']


@admin.register(ChallengeCompletion)
class ChallengeCompletionAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'completed_at']
    list_filter = ['challenge__challenge_type']
    search_fields = ['user__email']
