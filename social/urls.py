from django.urls import path
from . import views

urlpatterns = [
    path('discussions/<slug:module_slug>/', views.ModuleDiscussionsView.as_view(), name='module-discussions'),
    path('discussions/<int:pk>/detail/', views.DiscussionDetailView.as_view(), name='discussion-detail'),
    path('discussions/<int:pk>/upvote/', views.UpvoteView.as_view(), name='upvote'),
    path('replies/<int:pk>/best/', views.MarkBestAnswerView.as_view(), name='best-answer'),
]
