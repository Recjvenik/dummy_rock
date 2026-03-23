from django.urls import path
from . import views

urlpatterns = [
    path('neural-network/', views.NeuralNetworkSimView.as_view(), name='sim-neural-network'),
    path('gradient-descent/', views.GradientDescentSimView.as_view(), name='sim-gradient-descent'),
    path('activation-functions/', views.ActivationFunctionSimView.as_view(), name='sim-activation'),
    path('bias-variance/', views.BiasVarianceSimView.as_view(), name='sim-bias-variance'),
    path('llm-params/', views.LLMParamsSimView.as_view(), name='sim-llm-params'),
    path('rag-pipeline/', views.RAGPipelineSimView.as_view(), name='sim-rag-pipeline'),
    path('agent-flow/', views.AgentFlowSimView.as_view(), name='sim-agent-flow'),
    path('tokenizer/', views.TokenizerSimView.as_view(), name='sim-tokenizer'),
    path('logic-gates/', views.LogicGatesSimView.as_view(), name='sim-logic-gates'),
    path('data-sorting/', views.DataSortingSimView.as_view(), name='sim-data-sorting'),
    path('pattern-recognition/', views.PatternRecognitionSimView.as_view(), name='sim-pattern-recognition'),
    path('kmeans/', views.KMeansSimView.as_view(), name='sim-kmeans'),
    path('decision-tree/', views.DecisionTreeSimView.as_view(), name='sim-decision-tree'),
    path('attention/', views.AttentionSimView.as_view(), name='sim-attention'),
    path('logs/', views.SimulationLogsView.as_view(), name='sim-logs'),
]
