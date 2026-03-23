import csv
from django.http import HttpResponse
from django.utils import timezone


def export_class_csv(classroom):
    """Generate a CSV HttpResponse for all students in a classroom."""
    response = HttpResponse(content_type='text/csv')
    filename = f"{classroom.name.replace(' ', '_')}_{timezone.now().strftime('%Y%m%d')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Email', 'Grade', 'XP', 'Level', 'Streak', 'Modules Completed', 'Last Active'])

    for student in classroom.students.all().order_by('first_name', 'last_name'):
        xp = level = streak = 0
        try:
            from gamification.models import UserXP
            xp_obj = UserXP.objects.filter(user=student).first()
            if xp_obj:
                xp = xp_obj.total_xp
                level = xp_obj.level
        except Exception:
            pass

        try:
            from gamification.models import DailyStreak
            streak_obj = DailyStreak.objects.filter(user=student).first()
            if streak_obj:
                streak = streak_obj.current_streak
        except Exception:
            pass

        try:
            from modules.models import UserProgress
            completed = UserProgress.objects.filter(user=student, completed=True).count()
            last_progress = UserProgress.objects.filter(user=student).order_by('-last_accessed').first()
            last_active = last_progress.last_accessed.date() if last_progress else ''
        except Exception:
            completed = 0
            last_active = ''

        writer.writerow([
            student.get_full_name() or student.username,
            student.email,
            getattr(student, 'grade', ''),
            xp,
            level,
            streak,
            completed,
            last_active,
        ])

    return response
