from django.contrib import admin
from .models import UserXP, XPEvent, Badge, UserBadge, DailyStreak


@admin.register(UserXP)
class UserXPAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_xp', 'level', 'level_title', 'last_activity']
    list_filter = ['level']
    search_fields = ['user__email']
    readonly_fields = ['level_title', 'xp_to_next_level', 'level_progress_pct']


@admin.register(XPEvent)
class XPEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'reason', 'created_at']
    list_filter = ['reason']
    search_fields = ['user__email']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'category', 'xp_reward', 'slug']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at']
    list_filter = ['badge__category']
    search_fields = ['user__email', 'badge__name']


@admin.register(DailyStreak)
class DailyStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'last_login_date', 'total_days']
    search_fields = ['user__email']
