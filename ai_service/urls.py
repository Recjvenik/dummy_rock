from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.AIChatView.as_view(), name='ai-chat'),
    path('explain/', views.ExplainConceptView.as_view(), name='ai-explain'),
    path('quiz/generate/', views.GenerateQuizView.as_view(), name='ai-quiz-generate'),
    path('code-review/', views.CodeReviewView.as_view(), name='ai-code-review'),
    path('code-explore/', views.CodeExploreView.as_view(), name='ai-code-explore'),
    path('index-codebase/', views.IndexCodebaseView.as_view(), name='ai-index-codebase'),
    path('learning-tips/', views.LearningTipsView.as_view(), name='ai-learning-tips'),
]
