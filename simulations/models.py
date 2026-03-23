from django.db import models
from django.conf import settings


class SimulationLog(models.Model):
    """Tracks all simulation runs with parameters and results"""
    SIMULATION_TYPES = [
        ('neural_network', 'Neural Network Visualizer'),
        ('gradient_descent', 'Gradient Descent'),
        ('activation_fn', 'Activation Function'),
        ('bias_variance', 'Bias-Variance Tradeoff'),
        ('linear_regression', 'Linear Regression'),
        ('classification', 'Classification Boundary'),
        ('decision_tree', 'Decision Tree'),
        ('cnn_visualizer', 'CNN Visualizer'),
        ('tokenizer', 'Tokenization Visualizer'),
        ('embedding', 'Embedding Explorer'),
        ('transformer', 'Transformer Architecture'),
        ('llm_params', 'LLM Parameter Playground'),
        ('rag_pipeline', 'RAG Pipeline Simulator'),
        ('agent_flow', 'Agent Flow Simulator'),
        ('fine_tuning', 'Fine-tuning Playground'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='simulation_logs')
    simulation_type = models.CharField(max_length=50, choices=SIMULATION_TYPES)
    parameters = models.JSONField(default=dict)
    result = models.JSONField(default=dict)
    simulated_latency_ms = models.FloatField(default=0)
    simulated_tokens = models.PositiveIntegerField(default=0)
    simulated_cost_usd = models.FloatField(default=0)
    session_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.simulation_type} - {self.created_at}"
