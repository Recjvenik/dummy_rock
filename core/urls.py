from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('learn/<slug:slug>/', views.module_learn, name='module-learn'),
    path('playground/', views.playground, name='playground'),
    path('rag-visualizer/', views.rag_visualizer, name='rag-visualizer'),
    path('agent-visualizer/', views.agent_visualizer, name='agent-visualizer'),
    path('neural-network/', views.neural_network_lab, name='neural-network-lab'),
    path('llm-params/', views.llm_params_lab, name='llm-params-lab'),
    path('ai-chat/', views.ai_chat, name='ai-chat'),
    path('glossary/', views.glossary, name='glossary'),
    path('learning-paths/', views.learning_paths, name='learning-paths'),
    path('concept-explorer/', views.concept_explorer, name='concept-explorer'),
    path('practice-zone/', views.practice_zone, name='practice-zone'),
    path('kmeans/', views.kmeans_lab, name='kmeans-lab'),
    path('decision-tree/', views.decision_tree_lab, name='decision-tree-lab'),
    path('attention/', views.attention_lab, name='attention-lab'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('badges/', views.badges, name='badges'),
    path('logic-gates/', views.logic_gates_lab, name='logic-gates-lab'),
    path('data-sorting/', views.data_sorting_lab, name='data-sorting-lab'),
    path('pattern-recognition/', views.pattern_recognition_lab, name='pattern-recognition-lab'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('ui-showcase/', views.ui_showcase, name='ui-showcase'),
    path('python-editor/', views.python_editor, name='python-editor'),
]
