from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import UserXP, UserBadge, Badge, DailyStreak, XPEvent
from .signals import award_xp, check_and_award_badge


class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        top_users = UserXP.objects.select_related('user').order_by('-total_xp')[:20]
        data = []
        for rank, uxp in enumerate(top_users, 1):
            badge_count = UserBadge.objects.filter(user=uxp.user).count()
            data.append({
                'rank': rank,
                'username': uxp.user.email.split('@')[0],
                'level': uxp.level,
                'level_title': uxp.level_title,
                'total_xp': uxp.total_xp,
                'badge_count': badge_count,
                'level_progress_pct': uxp.level_progress_pct,
            })

        current_rank = None
        if request.user.is_authenticated:
            try:
                uxp = UserXP.objects.get(user=request.user)
                above = UserXP.objects.filter(total_xp__gt=uxp.total_xp).count()
                current_rank = above + 1
            except UserXP.DoesNotExist:
                pass

        return Response({'leaderboard': data, 'current_rank': current_rank})


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        xp, _ = UserXP.objects.get_or_create(user=request.user)
        streak, _ = DailyStreak.objects.get_or_create(user=request.user)
        badge_count = UserBadge.objects.filter(user=request.user).count()
        recent_events = XPEvent.objects.filter(user=request.user)[:10]
        rank = UserXP.objects.filter(total_xp__gt=xp.total_xp).count() + 1

        return Response({
            'rank': rank,
            'total_xp': xp.total_xp,
            'level': xp.level,
            'level_title': xp.level_title,
            'xp_to_next_level': xp.xp_to_next_level,
            'level_progress_pct': xp.level_progress_pct,
            'current_streak': streak.current_streak,
            'longest_streak': streak.longest_streak,
            'total_days': streak.total_days,
            'badge_count': badge_count,
            'recent_events': [
                {'amount': e.amount, 'reason': e.reason, 'created_at': e.created_at.isoformat()}
                for e in recent_events
            ],
        })


class AwardXPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reason = request.data.get('reason', 'action')
        XP_MAP = {
            'module_complete': 50, 'section_complete': 10, 'quiz_pass': 25,
            'quiz_perfect': 50, 'simulation_run': 5, 'daily_login': 15,
            'streak_7': 100, 'streak_30': 500, 'code_explore': 3, 'first_module': 25,
        }
        amount = XP_MAP.get(reason, 5)
        new_total = award_xp(request.user, amount, reason)

        # Check streak badges
        streak, _ = DailyStreak.objects.get_or_create(user=request.user)
        streak_len, is_new_day = streak.record_login()
        if streak_len >= 7:
            check_and_award_badge(request.user, 'streak_7')
        if streak_len >= 30:
            check_and_award_badge(request.user, 'streak_30')

        return Response({'xp_awarded': amount, 'total_xp': new_total, 'reason': reason})


class UserBadgesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_badges = Badge.objects.all()
        earned_slugs = set(UserBadge.objects.filter(
            user=request.user
        ).values_list('badge__slug', flat=True))

        earned = []
        locked = []
        for badge in all_badges:
            item = {
                'slug': badge.slug,
                'name': badge.name,
                'description': badge.description,
                'icon': badge.icon,
                'color': badge.color,
                'xp_reward': badge.xp_reward,
                'category': badge.category,
            }
            if badge.slug in earned_slugs:
                ub = UserBadge.objects.get(user=request.user, badge=badge)
                item['awarded_at'] = ub.awarded_at.isoformat()
                earned.append(item)
            else:
                locked.append(item)

        return Response({'earned': earned, 'locked': locked, 'total_earned': len(earned)})
