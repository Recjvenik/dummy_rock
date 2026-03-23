from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .engine import (
    simulate_neural_network, simulate_gradient_descent,
    simulate_activation_functions, simulate_bias_variance,
    simulate_llm_params, simulate_rag_pipeline,
    simulate_agent_flow, simulate_tokenizer, log_simulation,
    simulate_logic_gates, simulate_data_sorting, simulate_pattern_recognition,
    simulate_kmeans, simulate_decision_tree, simulate_attention,
)
from .models import SimulationLog


class NeuralNetworkSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_neural_network(params)
        log_simulation(request.user, 'neural_network', params, result,
                       latency=50, tokens=0, cost=0,
                       session_id=request.session.session_key or '')
        return Response(result)


class GradientDescentSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_gradient_descent(params)
        log_simulation(request.user, 'gradient_descent', params, result, 30, 0, 0)
        return Response(result)


class ActivationFunctionSimView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = simulate_activation_functions({})
        return Response(result)


class BiasVarianceSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_bias_variance(params)
        log_simulation(request.user, 'bias_variance', params, result, 20, 0, 0)
        return Response(result)


class LLMParamsSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_llm_params(params)
        log_simulation(request.user, 'llm_params', params, result,
                       result.get('latency_ms', 0),
                       result.get('estimated_tokens', 0),
                       result.get('cost_usd', 0))
        return Response(result)


class RAGPipelineSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_rag_pipeline(params)
        log_simulation(request.user, 'rag_pipeline', params, result,
                       result.get('total_latency_ms', 0),
                       result.get('total_tokens', 0),
                       result.get('cost_usd', 0))
        return Response(result)


class AgentFlowSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_agent_flow(params)
        log_simulation(request.user, 'agent_flow', params, result,
                       result.get('total_latency_ms', 0),
                       result.get('total_tokens', 0),
                       result.get('cost_usd', 0))
        return Response(result)


class TokenizerSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_tokenizer(params)
        log_simulation(request.user, 'tokenizer', params, result, 10, result.get('token_count', 0), 0)
        return Response(result)


class LogicGatesSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = simulate_logic_gates(request.data)
        log_simulation(request.user, 'logic_gates', request.data, result, 5, 0, 0)
        return Response(result)


class DataSortingSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = simulate_data_sorting(request.data)
        log_simulation(request.user, 'data_sorting', request.data, result, 10, 0, 0)
        return Response(result)


class PatternRecognitionSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = simulate_pattern_recognition(request.data)
        log_simulation(request.user, 'pattern_recognition', request.data, result, 5, 0, 0)
        return Response(result)


class KMeansSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_kmeans(params)
        log_simulation(request.user, 'kmeans', params, result, 50, 0, 0)
        return Response(result)


class DecisionTreeSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_decision_tree(params)
        log_simulation(request.user, 'decision_tree', params, result, 80, 0, 0)
        return Response(result)


class AttentionSimView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        params = request.data
        result = simulate_attention(params)
        log_simulation(request.user, 'attention', params, result, 60, 0, 0)
        return Response(result)


class SimulationLogsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sim_type = request.query_params.get('type', None)
        qs = SimulationLog.objects.filter(user=request.user if request.user.is_authenticated else None)
        if sim_type:
            qs = qs.filter(simulation_type=sim_type)
        data = list(qs.values('simulation_type', 'simulated_latency_ms',
                              'simulated_tokens', 'simulated_cost_usd', 'created_at')[:50])
        return Response(data)
