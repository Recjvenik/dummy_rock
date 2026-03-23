import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .engine import (simulate_neural_network, simulate_gradient_descent,
                     simulate_rag_pipeline, simulate_agent_flow)


class SimulationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({'type': 'connected', 'message': 'Simulation WS connected'}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        sim_type = data.get('type', '')
        params = data.get('params', {})

        await self.send(json.dumps({'type': 'status', 'message': f'Running {sim_type}...'}))

        if sim_type == 'rag_pipeline':
            await self._stream_rag(params)
        elif sim_type == 'agent_flow':
            await self._stream_agent(params)
        elif sim_type == 'gradient_descent':
            await self._stream_gradient(params)
        elif sim_type == 'neural_network':
            result = simulate_neural_network(params)
            await self.send(json.dumps({'type': 'result', 'data': result}))
        else:
            await self.send(json.dumps({'type': 'error', 'message': f'Unknown simulation: {sim_type}'}))

    async def _stream_rag(self, params):
        """Stream RAG pipeline stages one by one"""
        from .engine import simulate_rag_pipeline
        result = simulate_rag_pipeline(params)
        for stage in result['stages']:
            await asyncio.sleep(stage['latency_ms'] / 1000)
            await self.send(json.dumps({'type': 'rag_stage', 'stage': stage}))
        await self.send(json.dumps({'type': 'rag_complete', 'summary': {
            'total_latency_ms': result['total_latency_ms'],
            'total_tokens': result['total_tokens'],
            'cost_usd': result['cost_usd'],
            'retrieved_chunks': result['retrieved_chunks'],
        }}))

    async def _stream_agent(self, params):
        """Stream agent steps one by one"""
        from .engine import simulate_agent_flow
        result = simulate_agent_flow(params)
        for step in result['steps']:
            await asyncio.sleep(min(step['latency_ms'] / 1000, 0.8))
            await self.send(json.dumps({'type': 'agent_step', 'step': step}))
        await self.send(json.dumps({'type': 'agent_complete', 'summary': {
            'total_latency_ms': result['total_latency_ms'],
            'total_tokens': result['total_tokens'],
            'cost_usd': result['cost_usd'],
            'tools_used': result['tools_used'],
        }}))

    async def _stream_gradient(self, params):
        """Stream gradient descent epoch by epoch"""
        from .engine import simulate_gradient_descent
        result = simulate_gradient_descent(params)
        for point in result['path']:
            await asyncio.sleep(0.05)
            await self.send(json.dumps({'type': 'gradient_step', 'point': point}))
        await self.send(json.dumps({'type': 'gradient_complete', 'result': result}))
