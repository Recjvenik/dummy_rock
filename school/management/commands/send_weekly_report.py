"""
Management command: send_weekly_report

Sends weekly progress emails to students and teachers.

Usage:
    python manage.py send_weekly_report
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from school.models import School, Classroom
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Send weekly progress emails to students and class summary to teachers.'

    def handle(self, *args, **options):
        week_ago = timezone.now() - timedelta(days=7)
        sent_students = 0
        sent_teachers = 0

        for classroom in Classroom.objects.select_related('school', 'teacher').prefetch_related('students'):
            self._send_student_emails(classroom, week_ago)
            sent_students += classroom.students.count()
            if classroom.teacher:
                self._send_teacher_email(classroom, week_ago)
                sent_teachers += 1

        self.stdout.write(self.style.SUCCESS(
            f'Weekly report sent: {sent_students} student emails, {sent_teachers} teacher emails.'
        ))

    def _send_student_emails(self, classroom, since):
        for student in classroom.students.all():
            try:
                xp_this_week = self._get_xp_this_week(student, since)
                streak = self._get_streak(student)
                send_mail(
                    subject=f'Your AI Lab Week — {classroom.school.name}',
                    message=self._student_body(student, xp_this_week, streak),
                    from_email='noreply@ailab.in',
                    recipient_list=[student.email],
                    fail_silently=True,
                )
            except Exception:
                pass

    def _send_teacher_email(self, classroom, since):
        try:
            students = list(classroom.students.all())
            top_3 = self._top_students(students)
            inactive = self._inactive_students(students, since)
            send_mail(
                subject=f'Weekly Class Summary — {classroom.name}',
                message=self._teacher_body(classroom, top_3, inactive),
                from_email='noreply@ailab.in',
                recipient_list=[classroom.teacher.email],
                fail_silently=True,
            )
        except Exception:
            pass

    def _get_xp_this_week(self, user, since):
        try:
            from gamification.models import XPEvent
            return sum(e.amount for e in XPEvent.objects.filter(user=user, created_at__gte=since))
        except Exception:
            return 0

    def _get_streak(self, user):
        try:
            from gamification.models import UserProfile
            return UserProfile.objects.get(user=user).streak_days
        except Exception:
            return 0

    def _top_students(self, students):
        ranked = []
        for s in students:
            try:
                from gamification.models import UserProfile
                xp = UserProfile.objects.get(user=s).total_xp
            except Exception:
                xp = 0
            ranked.append((s, xp))
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked[:3]

    def _inactive_students(self, students, since):
        inactive = []
        for s in students:
            try:
                from gamification.models import UserProgress
                recent = UserProgress.objects.filter(user=s, last_accessed__gte=since).exists()
                if not recent:
                    inactive.append(s)
            except Exception:
                pass
        return inactive

    def _student_body(self, student, xp, streak):
        name = student.first_name or student.email.split('@')[0]
        return f"""Hi {name},

Here's your AI Lab week summary:

📈 XP earned this week: {xp}
🔥 Current streak: {streak} days

Keep going — consistency is the key to mastering AI!

Visit https://ailab.in to continue learning.

— The AI Lab Team
"""

    def _teacher_body(self, classroom, top_3, inactive):
        top_str = '\n'.join(
            f"  {i+1}. {s.get_full_name() or s.email} — {xp} XP"
            for i, (s, xp) in enumerate(top_3)
        ) or '  No data available.'
        inactive_str = ', '.join(s.get_full_name() or s.email for s in inactive) or 'None — great week!'
        return f"""Hi {classroom.teacher.first_name or classroom.teacher.email},

Weekly summary for {classroom.name}:

🏆 Top 3 Students:
{top_str}

😴 No activity this week:
  {inactive_str}

Log in at https://ailab.in/school/ to see full details and export CSV reports.

— AI Lab Platform
"""
