import json
import boto3
from django.conf import settings


class BedrockClient:
    """AWS Bedrock Claude client for AI Lab"""

    def __init__(self):
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.model_id = settings.BEDROCK_MODEL_ID

    def chat(self, messages: list, system: str = '', max_tokens: int = 1024,
             temperature: float = 0.7) -> dict:
        """Send a chat request and return full response"""
        body = {
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': max_tokens,
            'temperature': temperature,
            'messages': messages,
        }
        if system:
            body['system'] = system

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
        )
        result = json.loads(response['body'].read())
        text = result['content'][0]['text'] if result.get('content') else ''
        usage = result.get('usage', {})
        return {
            'text': text,
            'input_tokens': usage.get('input_tokens', 0),
            'output_tokens': usage.get('output_tokens', 0),
            'stop_reason': result.get('stop_reason', ''),
        }

    def stream_chat(self, messages: list, system: str = '', max_tokens: int = 1024,
                    temperature: float = 0.7):
        """Stream responses from Bedrock — yields text chunks"""
        body = {
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': max_tokens,
            'temperature': temperature,
            'messages': messages,
        }
        if system:
            body['system'] = system

        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=json.dumps(body),
        )

        for event in response['body']:
            chunk = json.loads(event['chunk']['bytes'])
            if chunk.get('type') == 'content_block_delta':
                delta = chunk.get('delta', {})
                if delta.get('type') == 'text_delta':
                    yield delta.get('text', '')
            elif chunk.get('type') == 'message_delta':
                usage = chunk.get('usage', {})
                yield {'__meta__': True, 'output_tokens': usage.get('output_tokens', 0)}


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    """Estimate cost for Claude Opus 4.5 on Bedrock (per token pricing estimate)"""
    input_cost_per_1k = 0.015
    output_cost_per_1k = 0.075
    return round(
        (input_tokens / 1000) * input_cost_per_1k +
        (output_tokens / 1000) * output_cost_per_1k, 6
    )


# Singleton client
_bedrock_client = None


def get_bedrock_client() -> BedrockClient:
    global _bedrock_client
    if _bedrock_client is None:
        _bedrock_client = BedrockClient()
    return _bedrock_client


# ─── System Prompts per AI topic ──────────────────────────────────────────────
SYSTEM_PROMPTS = {
    'default': """You are an AI learning assistant for AI Lab — an interactive platform teaching 
AI from basics to agentic systems. You explain concepts clearly, use analogies, 
and provide code examples. Be concise, educational, and engaging.""",

    'ai_basics': """You are an AI expert teaching AI fundamentals. Explain neural networks, 
ML concepts, and deep learning with clear analogies and visual explanations. 
Use beginner-friendly language but include technical depth when asked.""",

    'rag': """You are a RAG architecture expert. Help users understand retrieval-augmented 
generation, vector databases, chunking strategies, re-ranking, and how to build 
production RAG systems. Include practical examples and real-world considerations.""",

    'agent': """You are an agentic AI expert. Explain multi-agent systems, planning, 
tool use, memory management, ReAct patterns, and CrewAI-style frameworks. 
Help users understand autonomous AI agent design.""",

    'llm': """You are an LLM systems expert. Help users understand transformer architecture, 
attention mechanisms, tokenization, fine-tuning, prompt engineering, and LLM optimization. 
Discuss production concerns like latency, cost, and reliability.""",
}
