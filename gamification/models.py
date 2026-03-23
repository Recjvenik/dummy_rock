from django.db import models
from django.utils import timezone
from django.conf import settings


class UserXP(models.Model):
    XP_LEVELS = {
        1: 'Beginner', 2: 'Explorer', 3: 'Learner', 4: 'Practitioner',
        5: 'Expert', 6: 'Master', 7: 'Champion', 8: 'Legend', 9: 'Guru', 10: 'Genius'
    }

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp')
    total_xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    last_activity = models.DateTimeField(auto_now=True)

    def add_xp(self, amount, reason=''):
        self.total_xp += amount
        self.level = min(10, 1 + self.total_xp // 100)
        self.save()
        XPEvent.objects.create(user=self.user, amount=amount, reason=reason)
        return self.total_xp

    @property
    def level_title(self):
        return self.XP_LEVELS.get(self.level, 'Genius')

    @property
    def xp_to_next_level(self):
        if self.level >= 10:
            return 0
        return (self.level + 1) * 100 - self.total_xp

    @property
    def level_progress_pct(self):
        current_level_xp = (self.level - 1) * 100
        next_level_xp = self.level * 100
        progress = self.total_xp - current_level_xp
        return min(100, int((progress / (next_level_xp - current_level_xp)) * 100))

    def __str__(self):
        return f"{self.user} — Level {self.level} ({self.total_xp} XP)"


class XPEvent(models.Model):
    REASON_CHOICES = [
        ('module_complete', 'Module Complete'),
        ('section_complete', 'Section Complete'),
        ('quiz_pass', 'Quiz Pass'),
        ('quiz_perfect', 'Quiz Perfect Score'),
        ('simulation_run', 'Simulation Run'),
        ('daily_login', 'Daily Login'),
        ('streak_7', '7-Day Streak'),
        ('streak_30', '30-Day Streak'),
        ('code_explore', 'Code Explore'),
        ('first_module', 'First Module Started'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp_events')
    amount = models.IntegerField()
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} +{self.amount} XP ({self.reason})"


class Badge(models.Model):
    CATEGORY_CHOICES = [
        ('learn', 'Learning'),
        ('explore', 'Exploration'),
        ('social', 'Social'),
        ('streak', 'Streak'),
    ]

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    icon = models.CharField(max_length=10)
    color = models.CharField(max_length=20, default='#00ff88')
    xp_reward = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='learn')

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-awarded_at']

    def __str__(self):
        return f"{self.user} — {self.badge.name}"


class DailyStreak(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)
    total_days = models.IntegerField(default=0)

    def record_login(self):
        today = timezone.now().date()
        if self.last_login_date == today:
            return self.current_streak, False  # Already logged today

        is_new_day = True
        if self.last_login_date and (today - self.last_login_date).days == 1:
            self.current_streak += 1
        else:
            self.current_streak = 1

        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_login_date = today
        self.total_days += 1
        self.save()
        return self.current_streak, is_new_day

    def __str__(self):
        return f"{self.user} — {self.current_streak} day streak"
