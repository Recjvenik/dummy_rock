from django.urls import path
from . import views

urlpatterns = [
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('stats/', views.UserStatsView.as_view(), name='user-stats'),
    path('award-xp/', views.AwardXPView.as_view(), name='award-xp'),
    path('badges/', views.UserBadgesView.as_view(), name='user-badges'),
]
