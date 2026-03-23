import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .bedrock import get_bedrock_client, SYSTEM_PROMPTS, estimate_cost
import asyncio


class AIAssistantConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for streaming AI chat responses from Claude via Bedrock"""

    async def connect(self):
        await self.accept()
        await self.send(json.dumps({
            'type': 'connected',
            'message': 'AI Assistant connected. Ask me anything about AI!'
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message', '')
            history = data.get('history', [])
            topic = data.get('topic', 'default')
            temperature = float(data.get('temperature', 0.7))
            max_tokens = int(data.get('max_tokens', 1024))

            if not message.strip():
                await self.send(json.dumps({'type': 'error', 'message': 'Empty message'}))
                return

            # Build message history
            messages = []
            for h in history[-10:]:  # Keep last 10 messages
                messages.append({'role': h['role'], 'content': h['content']})
            messages.append({'role': 'user', 'content': message})

            system = SYSTEM_PROMPTS.get(topic, SYSTEM_PROMPTS['default'])

            await self.send(json.dumps({'type': 'stream_start'}))

            # Stream in executor to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            client = get_bedrock_client()

            full_text = ''
            input_tokens = len(' '.join(m['content'] for m in messages).split())  # estimate
            output_tokens = 0

            def run_stream():
                chunks = []
                meta = {}
                for chunk in client.stream_chat(messages, system, max_tokens, temperature):
                    if isinstance(chunk, dict) and chunk.get('__meta__'):
                        meta = chunk
                    else:
                        chunks.append(chunk)
                return chunks, meta

            chunks, meta = await loop.run_in_executor(None, run_stream)

            for chunk in chunks:
                full_text += chunk
                await self.send(json.dumps({'type': 'stream_chunk', 'text': chunk}))
                await asyncio.sleep(0)  # Yield control

            output_tokens = meta.get('output_tokens', len(full_text.split()))
            cost = estimate_cost(input_tokens, output_tokens)

            await self.send(json.dumps({
                'type': 'stream_end',
                'full_text': full_text,
                'metrics': {
                    'input_tokens': input_tokens,
                    'output_tokens': output_tokens,
                    'cost_usd': cost,
                }
            }))

        except Exception as e:
            await self.send(json.dumps({
                'type': 'error',
                'message': f'AI service error: {str(e)}'
            }))
