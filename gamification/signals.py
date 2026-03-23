from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_gamification(sender, instance, created, **kwargs):
    if created:
        from .models import UserXP, DailyStreak
        UserXP.objects.get_or_create(user=instance)
        DailyStreak.objects.get_or_create(user=instance)


def award_xp(user, amount, reason):
    """Utility to safely award XP to a user."""
    from .models import UserXP
    try:
        xp, _ = UserXP.objects.get_or_create(user=user)
        return xp.add_xp(amount, reason)
    except Exception:
        return 0


def check_and_award_badge(user, badge_slug):
    """Award a badge if not already earned."""
    from .models import Badge, UserBadge, UserXP
    try:
        badge = Badge.objects.get(slug=badge_slug)
        awarded, created = UserBadge.objects.get_or_create(user=user, badge=badge)
        if created and badge.xp_reward > 0:
            xp, _ = UserXP.objects.get_or_create(user=user)
            xp.add_xp(badge.xp_reward, f'badge_{badge_slug}')
        return created
    except Badge.DoesNotExist:
        return False
