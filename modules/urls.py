from django.urls import path
from . import views

urlpatterns = [
    path('', views.ModuleListView.as_view(), name='module-list'),
    path('concepts/', views.ConceptListView.as_view(), name='concept-list'),
    path('progress/', views.UserProgressListView.as_view(), name='user-progress'),
    path('dashboard/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('<slug:slug>/', views.ModuleDetailView.as_view(), name='module-detail'),
    path('<slug:module_slug>/progress/', views.UserProgressUpdateView.as_view(), name='module-progress'),
    path('<slug:module_slug>/quiz/', views.QuizQuestionsView.as_view(), name='quiz-questions'),
    path('<slug:module_slug>/quiz/submit/', views.QuizSubmitView.as_view(), name='quiz-submit'),
]
