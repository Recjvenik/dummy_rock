import random
import string
from django.db import models
from django.conf import settings
from django.utils import timezone


def _generate_join_code():
    """Generate an 8-character alphanumeric join code like AILAB8C3."""
    chars = string.ascii_uppercase + string.digits
    return 'AILAB' + ''.join(random.choices(chars, k=3))


class School(models.Model):
    BOARD_CHOICES = [
        ('cbse', 'CBSE'),
        ('icse', 'ICSE'),
        ('state', 'State Board'),
        ('ib', 'IB'),
        ('other', 'Other'),
    ]
    TIER_CHOICES = [
        ('free', 'Free Trial'),
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    city = models.CharField(max_length=100)
    board = models.CharField(max_length=10, choices=BOARD_CHOICES, default='cbse')
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True)
    subscription_tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='free')
    max_students = models.PositiveIntegerField(default=50)
    subscription_start = models.DateField(null=True, blank=True)
    subscription_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        if self.subscription_tier == 'free':
            return True
        if self.subscription_end is None:
            return False
        return self.subscription_end >= timezone.now().date()


class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='taught_classrooms')
    name = models.CharField(max_length=100, help_text='e.g. Class 10-A AI Section')
    grade = models.PositiveSmallIntegerField(choices=[(g, f'Class {g}') for g in range(8, 13)])
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_classrooms', blank=True)
    join_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['grade', 'name']

    def __str__(self):
        return f"{self.name} ({self.school.name})"

    def save(self, *args, **kwargs):
        if not self.join_code:
            code = _generate_join_code()
            while Classroom.objects.filter(join_code=code).exists():
                code = _generate_join_code()
            self.join_code = code
        super().save(*args, **kwargs)


class Assignment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    module = models.ForeignKey('modules.Module', on_delete=models.SET_NULL, null=True, related_name='assignments')
    title = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_assignments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.classroom.name}"

    @property
    def completion_count(self):
        """Count how many classroom students have completed the assigned module."""
        from modules.models import UserProgress
        student_ids = self.classroom.students.values_list('id', flat=True)
        return UserProgress.objects.filter(
            user_id__in=student_ids,
            module=self.module,
            completed=True
        ).count()


class DailyChallenge(models.Model):
    CHALLENGE_TYPES = [
        ('quiz', 'Quiz'),
        ('lab', 'Lab'),
        ('glossary', 'Glossary'),
        ('streak', 'Streak'),
    ]

    date = models.DateField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES, default='quiz')
    target_module = models.ForeignKey('modules.Module', on_delete=models.SET_NULL, null=True, blank=True, related_name='daily_challenges')
    xp_reward = models.PositiveIntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Challenge {self.date}: {self.title}"


class ChallengeCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='challenge_completions')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE, related_name='completions')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.email} → {self.challenge.title}"
