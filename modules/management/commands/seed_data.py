from django.core.management.base import BaseCommand
from django.utils.text import slugify
from modules.models import Module, Section, Concept, QuizQuestion


MODULES_DATA = [
    {
        'order': 1, 'title': 'AI Basics',
        'subtitle': 'Start here — understand AI from the ground up through animations and interactive examples.',
        'description': 'What is AI? ML vs DL vs AI. Supervised vs Unsupervised. Neural Network foundations.',
        'difficulty': 'beginner', 'tag': 'beginner', 'icon': '🟢', 'color': '#00ff88',
        'estimated_time': 30,
        'sections': [
            {'order': 1, 'title': 'What is Artificial Intelligence?',
             'content_md': 'Artificial Intelligence (AI) is the simulation of human intelligence by machines.\n\nAI systems learn from data, identify patterns, and make decisions — often with minimal human intervention.\n\n**Three waves of AI:**\n- Rule-based systems (1950s–1980s)\n- Machine Learning (1990s–2010s)  \n- Deep Learning & Foundation Models (2010s–present)',
             'key_insight': 'AI is not magic — it\'s pattern recognition at scale, powered by data and compute.',
             'has_visualizer': False},
            {'order': 2, 'title': 'ML vs DL vs AI',
             'content_md': '**AI** is the broad concept.\n**Machine Learning** is a subset: algorithms that learn from data.\n**Deep Learning** is a subset of ML: neural networks with many layers.\n\nThe relationship:\nAI ⊃ ML ⊃ Deep Learning ⊃ Large Language Models',
             'key_insight': 'Every Deep Learning model IS a Machine Learning model IS an AI system.',
             'has_visualizer': False},
            {'order': 3, 'title': 'Neural Network Basics',
             'content_md': 'A neural network is a collection of connected nodes (neurons), organized in layers:\n\n1. **Input Layer** — receives raw data\n2. **Hidden Layers** — learn internal representations\n3. **Output Layer** — produces predictions\n\nEach neuron applies a weighted sum + activation function:\n`output = activation(w₁x₁ + w₂x₂ + ... + b)`',
             'key_insight': 'Neurons don\'t "think" — they compute weighted sums and pass the result through a non-linear function.',
             'has_visualizer': True, 'visualizer_type': 'neural_network'},
            {'order': 4, 'title': 'Supervised vs Unsupervised Learning',
             'content_md': '**Supervised Learning**: Learns from labeled examples (input → output pairs)\n- Classification, Regression\n- Examples: spam detection, price prediction\n\n**Unsupervised Learning**: Finds patterns in unlabeled data\n- Clustering, Dimensionality reduction\n- Examples: customer segmentation, anomaly detection\n\n**Reinforcement Learning**: Learns by reward/punishment\n- Agent, Environment, Reward\n- Examples: game playing, robotics',
             'key_insight': 'Most production AI today is supervised learning — label your data carefully!',
             'has_visualizer': False},
        ],
        'concepts': ['Neural Network', 'Supervised Learning', 'Unsupervised Learning', 'Activation Function', 'Bias-Variance Tradeoff'],
        'quiz': [
            {'question': 'Which is the correct hierarchy?', 'option_a': 'ML ⊃ AI ⊃ DL', 'option_b': 'AI ⊃ ML ⊃ DL', 'option_c': 'DL ⊃ ML ⊃ AI', 'option_d': 'All are equal', 'correct_answer': 'b', 'explanation': 'AI is the broadest field, ML is a subset of AI, and Deep Learning is a subset of ML.', 'difficulty': 'beginner'},
            {'question': 'What does a neuron compute?', 'option_a': 'Random output', 'option_b': 'Weighted sum + activation function', 'option_c': 'Max of all inputs', 'option_d': 'Average of inputs', 'correct_answer': 'b', 'explanation': 'A neuron computes a weighted sum of inputs, adds a bias, then passes through an activation function.', 'difficulty': 'beginner'},
        ]
    },
    {
        'order': 2, 'title': 'Machine Learning Deep Dive',
        'subtitle': 'Linear regression, classification, decision trees, and feature engineering explored interactively.',
        'description': 'Linear Regression, Classification Boundaries, Decision Trees, Random Forests, Cross-validation.',
        'difficulty': 'intermediate', 'tag': 'interactive', 'icon': '🟡', 'color': '#ffd700',
        'estimated_time': 45,
        'sections': [
            {'order': 1, 'title': 'Linear Regression Playground',
             'content_md': 'Linear regression finds the best-fit line through data points.\n\n**Formula:** y = mx + b\n\nWhere:\n- m = slope (weight)\n- b = intercept (bias)\n- Minimize: Mean Squared Error (MSE)\n\n**Gradient descent** iteratively updates weights:\n`w = w - α × ∂L/∂w`',
             'key_insight': 'Linear regression is the foundation of all neural networks — learn it deeply.',
             'has_visualizer': True, 'visualizer_type': 'gradient_descent'},
            {'order': 2, 'title': 'Gradient Descent',
             'content_md': 'Gradient descent is the optimization algorithm that trains almost every ML model.\n\n**Steps:**\n1. Start at random weights\n2. Compute loss (error)\n3. Calculate gradient (direction of steepest increase)\n4. Step in the opposite direction\n5. Repeat until convergence\n\n**Learning rate** controls step size — too large: overshoot; too small: too slow.',
             'key_insight': 'The learning rate is the most important hyperparameter in training.',
             'has_visualizer': True, 'visualizer_type': 'gradient_descent'},
            {'order': 3, 'title': 'Bias-Variance Tradeoff',
             'content_md': '**Bias**: Error from wrong assumptions (underfitting)\n**Variance**: Error from sensitivity to noise (overfitting)\n\nTotal Error = Bias² + Variance + Irreducible Noise\n\n- High bias → simple model, learns too little\n- High variance → complex model, memorizes training data\n- **Goal**: find the sweet spot',
             'key_insight': 'More data reduces variance. Better features reduce bias.',
             'has_visualizer': True, 'visualizer_type': 'bias_variance'},
        ],
        'concepts': ['Gradient Descent', 'Loss Function', 'Overfitting', 'Regularization', 'Cross-validation', 'Decision Tree'],
        'quiz': [
            {'question': 'High bias typically indicates:', 'option_a': 'Overfitting', 'option_b': 'Underfitting', 'option_c': 'Perfect fit', 'option_d': 'Data problem', 'correct_answer': 'b', 'explanation': 'High bias means the model is too simple and underfits the training data.', 'difficulty': 'intermediate'},
        ]
    },
    {
        'order': 3, 'title': 'Deep Learning Lab',
        'subtitle': 'Neural network builder, CNN visualizer, RNN flows, and backpropagation simulator.',
        'description': 'Deep Neural Networks, CNNs for vision, RNNs for sequences, Attention, Backpropagation.',
        'difficulty': 'intermediate', 'tag': 'deep-dive', 'icon': '🔵', 'color': '#4d96ff',
        'estimated_time': 60,
        'sections': [
            {'order': 1, 'title': 'Deep Neural Networks',
             'content_md': 'Deep Neural Networks (DNNs) have multiple hidden layers that learn hierarchical representations.\n\n**Layer types:**\n- Dense/Fully Connected\n- Convolutional (CNN) — spatial patterns\n- Recurrent (RNN) — sequences\n- Attention — global dependencies\n\n**Key insight**: Each layer learns increasingly abstract features.',
             'key_insight': 'Early layers learn edges, middle layers learn shapes, deep layers learn concepts.',
             'has_visualizer': True, 'visualizer_type': 'neural_network'},
            {'order': 2, 'title': 'Backpropagation',
             'content_md': 'Backpropagation computes gradients efficiently using the chain rule.\n\n**Forward pass**: compute predictions\n**Backward pass**: compute gradients layer by layer\n\nKey formula (chain rule):\n`∂L/∂w = ∂L/∂y × ∂y/∂w`\n\nThis is how neural networks learn from their mistakes.',
             'key_insight': 'Backprop is just the chain rule of calculus applied systematically through the network.',
             'has_visualizer': False},
        ],
        'concepts': ['CNN', 'RNN', 'Backpropagation', 'Attention', 'BatchNorm', 'Dropout'],
        'quiz': []
    },
    {
        'order': 4, 'title': 'Generative AI',
        'subtitle': 'Tokenization, embeddings, transformer architecture, temperature, and fine-tuning explored interactively.',
        'description': 'Tokenization, Embedding Space, Transformer Architecture, Temperature/Top-k/Top-p, Fine-tuning.',
        'difficulty': 'advanced', 'tag': 'simulator', 'icon': '🟣', 'color': '#b15eff',
        'estimated_time': 60,
        'sections': [
            {'order': 1, 'title': 'Tokenization Visualizer',
             'content_md': 'Tokenization splits text into tokens — the atomic units LLMs process.\n\n**Types:**\n- Word-level: "Hello world" → ["Hello", "world"]\n- BPE (Byte Pair Encoding): "Hello" → ["He", "llo"]\n- SentencePiece: language-agnostic\n\nGPT-4 uses ~100K tokens in its vocabulary.\n\nKey metric: **Tokens per second** = throughput.',
             'key_insight': 'LLMs don\'t read words — they read tokens. "unbelievable" might be 3 tokens.',
             'has_visualizer': True, 'visualizer_type': 'tokenizer'},
            {'order': 2, 'title': 'Transformer Architecture',
             'content_md': 'The Transformer (2017, "Attention is All You Need") revolutionized AI.\n\n**Key components:**\n- Multi-head self-attention\n- Positional encoding\n- Feed-forward layers\n- Layer normalization\n- Residual connections\n\n**Attention formula:**\n`Attention(Q,K,V) = softmax(QKᵀ/√d)V`',
             'key_insight': 'Self-attention lets every token attend to every other token simultaneously — no sequential bottleneck.',
             'has_visualizer': False},
            {'order': 3, 'title': 'Temperature, Top-K, Top-P',
             'content_md': '**Temperature**: controls randomness of output distribution\n- Low (0.1): very focused, deterministic\n- High (1.5): random, creative\n\n**Top-K**: only sample from top K most likely tokens\n\n**Top-P** (nucleus sampling): sample from tokens whose cumulative probability ≥ P\n\nThese are **inference parameters** — they don\'t change model weights.',
             'key_insight': 'Temperature is the most impactful parameter for controlling creativity vs accuracy.',
             'has_visualizer': True, 'visualizer_type': 'llm_params'},
        ],
        'concepts': ['Tokenization', 'BPE', 'Transformer', 'Attention', 'Temperature', 'Top-K', 'Top-P', 'Embedding', 'Fine-tuning'],
        'quiz': [
            {'question': 'What does temperature=0 mean for an LLM?', 'option_a': 'Maximum randomness', 'option_b': 'Model crashes', 'option_c': 'Always picks the most likely token (greedy)', 'option_d': 'No output', 'correct_answer': 'c', 'explanation': 'Temperature=0 makes the model deterministic — it always picks the highest probability token.', 'difficulty': 'intermediate'},
        ]
    },
    {
        'order': 5, 'title': 'LLM Systems',
        'subtitle': 'RAG architecture, vector databases, chunking strategies, re-ranking, and production LLM systems.',
        'description': 'RAG Architecture, Vector DB, Chunking, Retrieval Scoring, Re-ranking, Latency vs Accuracy.',
        'difficulty': 'advanced', 'tag': 'critical', 'icon': '🔴', 'color': '#ff4d6d',
        'estimated_time': 75,
        'sections': [
            {'order': 1, 'title': 'RAG Architecture',
             'content_md': 'Retrieval-Augmented Generation (RAG) combines retrieval with generation:\n\n**Flow:**\nUser Query → Embed Query → Vector Search → Retrieve Chunks → LLM + Context → Response\n\n**Why RAG?**\n- Reduces hallucinations\n- Adds up-to-date knowledge\n- Source-grounded answers\n- No retraining needed\n\n**Production considerations:**\n- Chunk size (256–1024 tokens)\n- Overlap between chunks\n- Embedding model choice\n- Re-ranking for precision',
             'key_insight': 'RAG is the most practical way to add domain knowledge to LLMs without fine-tuning.',
             'has_visualizer': True, 'visualizer_type': 'rag_pipeline'},
            {'order': 2, 'title': 'Vector Databases',
             'content_md': 'Vector databases store and search high-dimensional embeddings efficiently.\n\n**Popular options:**\n- **Pinecone** — fully managed, production-ready\n- **Weaviate** — open-source, multi-modal\n- **ChromaDB** — local-first, easy to start\n- **pgvector** — Postgres extension\n\n**Search algorithms:**\n- Cosine similarity\n- Euclidean distance\n- HNSW (Hierarchical Navigable Small World) for speed',
             'key_insight': 'Vector search finds semantically similar content, not just keyword matches.',
             'has_visualizer': False},
            {'order': 3, 'title': 'Chunking Strategies',
             'content_md': '**Fixed-size chunking**: simple, predictable\n**Sentence chunking**: preserves semantic boundaries\n**Semantic chunking**: embeddings-based splits\n**Recursive character splitting**: LangChain standard\n\n**Chunk size tradeoffs:**\n- Small chunks (128–256): precise retrieval, less context\n- Large chunks (1024–2048): more context, less precise\n- Overlap (10–20%): prevents losing context at boundaries',
             'key_insight': 'Chunk size is often the #1 factor affecting RAG quality. Always experiment.',
             'has_visualizer': False},
        ],
        'concepts': ['RAG', 'Vector Database', 'Embedding', 'Chunking', 'Re-ranking', 'Semantic Search', 'Pinecone', 'HNSW'],
        'quiz': []
    },
    {
        'order': 6, 'title': 'Agentic AI',
        'subtitle': 'Multi-agent flows, memory buffers, tool calling, planning vs reactive agents, and CrewAI patterns.',
        'description': 'Multi-Agent Systems, Memory, Tool Calling, Planning, ReAct Pattern, Cost vs Performance.',
        'difficulty': 'advanced', 'tag': 'simulator', 'icon': '🟠', 'color': '#ff8c00',
        'estimated_time': 90,
        'sections': [
            {'order': 1, 'title': 'What is an AI Agent?',
             'content_md': 'An AI agent is an LLM that can take actions in a loop:\n\n**Agent Loop:**\n1. Observe (input, memory, tool results)\n2. Think (LLM reasoning)\n3. Act (call tool or respond)\n4. Repeat until goal achieved\n\n**Tools agents can use:**\n- Web search\n- Code execution\n- API calls\n- File system\n- Other agents',
             'key_insight': 'An agent is just an LLM in a loop with access to tools and memory.',
             'has_visualizer': True, 'visualizer_type': 'agent_flow'},
            {'order': 2, 'title': 'ReAct Pattern',
             'content_md': 'ReAct = Reasoning + Acting\n\n**Format:**\nThought: [agent reasons about the situation]\nAction: [tool to call]\nObservation: [tool result]\nThought: [reason about observation]\n... repeat ...\nFinal Answer: [response]\n\nThis interleaving of reasoning and action is powerful for multi-step tasks.',
             'key_insight': 'Chain-of-thought + tool use = emergent problem solving.',
             'has_visualizer': False},
            {'order': 3, 'title': 'Memory in Agents',
             'content_md': '**Types of agent memory:**\n\n- **In-context (short-term)**: conversation history in the prompt window\n- **External (long-term)**: vector store, key-value store\n- **Episodic**: recent interactions\n- **Semantic**: facts and knowledge\n- **Procedural**: how to do tasks\n\n**Memory tradeoffs:**\n- More memory = more context = better performance\n- More context = higher tokens = higher cost + latency',
             'key_insight': 'Agent memory is the difference between a stateless chatbot and a true AI assistant.',
             'has_visualizer': False},
        ],
        'concepts': ['AI Agent', 'ReAct', 'Tool Calling', 'Memory', 'Multi-Agent', 'CrewAI', 'LangChain', 'Planning'],
        'quiz': [
            {'question': 'What does ReAct stand for?', 'option_a': 'Reactive Agents', 'option_b': 'Reasoning and Acting', 'option_c': 'Real-time Actions', 'option_d': 'Reinforced Acting', 'correct_answer': 'b', 'explanation': 'ReAct stands for Reasoning + Acting — interleaving thought steps with action calls.', 'difficulty': 'advanced'},
        ]
    },
    {
        'order': 7, 'title': 'AI Playground',
        'subtitle': 'Full sandbox — build RAG, tune LLMs, add tools, see token usage and latency live.',
        'description': 'Open sandbox: Build RAG, tune LLM parameters, add tools, see token usage, latency, cost.',
        'difficulty': 'advanced', 'tag': 'sandbox', 'icon': '🧪', 'color': '#00e5ff',
        'estimated_time': 120,
        'sections': [
            {'order': 1, 'title': 'Welcome to the Playground',
             'content_md': 'The AI Playground gives you full control over AI system parameters.\n\n**What you can do:**\n- Configure LLM parameters (temperature, model, tokens)\n- Run RAG pipeline with custom queries\n- Simulate agent flows with different tool configurations\n- Observe latency, token usage, and cost in real-time\n\nThis is your experimental lab — break things, learn from them.',
             'key_insight': 'The best way to understand AI systems is to run them with different configurations.',
             'has_visualizer': False},
        ],
        'concepts': ['Sandbox', 'Prompt Engineering', 'Token Budget', 'Cost Optimization'],
        'quiz': []
    },
]

ALL_CONCEPTS = [
    'Neural Network', 'Deep Learning', 'Machine Learning', 'Supervised Learning', 'Unsupervised Learning',
    'Reinforcement Learning', 'Gradient Descent', 'Backpropagation', 'Activation Function', 'Loss Function',
    'Overfitting', 'Underfitting', 'Regularization', 'Dropout', 'BatchNorm', 'CNN', 'RNN', 'LSTM',
    'Transformer', 'Attention', 'Self-Attention', 'Positional Encoding', 'Tokenization', 'BPE', 'Embedding',
    'Temperature', 'Top-K', 'Top-P', 'Fine-tuning', 'RLHF', 'Prompt Engineering', 'RAG', 'Vector Database',
    'Chunking', 'Re-ranking', 'Cosine Similarity', 'HNSW', 'Pinecone', 'ChromaDB', 'AI Agent', 'ReAct',
    'Tool Calling', 'Memory', 'Multi-Agent', 'LangChain', 'CrewAI', 'Planning', 'Hallucination',
    'Grounding', 'Context Window', 'Token Budget', 'Latency', 'Throughput', 'Inference', 'Training',
]


class Command(BaseCommand):
    help = 'Seed the database with AI Lab modules, sections, concepts, and quiz questions'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding AI Lab database...')

        # Create all concepts
        concept_objs = {}
        for c in ALL_CONCEPTS:
            obj, _ = Concept.objects.get_or_create(name=c)
            concept_objs[c] = obj
        self.stdout.write(f'  ✓ {len(ALL_CONCEPTS)} concepts created')

        # Create modules + sections + quiz
        for mod_data in MODULES_DATA:
            slug = slugify(mod_data['title'])
            module, created = Module.objects.update_or_create(
                slug=slug,
                defaults={
                    'order': mod_data['order'],
                    'title': mod_data['title'],
                    'subtitle': mod_data['subtitle'],
                    'description': mod_data['description'],
                    'difficulty': mod_data['difficulty'],
                    'tag': mod_data['tag'],
                    'icon': mod_data['icon'],
                    'color': mod_data['color'],
                    'estimated_time': mod_data['estimated_time'],
                    'is_published': True,
                }
            )
            action = 'Created' if created else 'Updated'

            # Sections
            for s in mod_data.get('sections', []):
                Section.objects.update_or_create(
                    module=module, order=s['order'],
                    defaults={
                        'title': s['title'],
                        'content_md': s['content_md'],
                        'key_insight': s.get('key_insight', ''),
                        'has_visualizer': s.get('has_visualizer', False),
                        'visualizer_type': s.get('visualizer_type', ''),
                    }
                )

            # Concepts
            for c_name in mod_data.get('concepts', []):
                if c_name in concept_objs:
                    module.concepts.add(concept_objs[c_name])

            # Quiz
            for i, q in enumerate(mod_data.get('quiz', [])):
                QuizQuestion.objects.update_or_create(
                    module=module, order=i,
                    defaults={
                        'question_type': 'mcq',
                        'question': q['question'],
                        'option_a': q['option_a'],
                        'option_b': q['option_b'],
                        'option_c': q.get('option_c', ''),
                        'option_d': q.get('option_d', ''),
                        'correct_answer': q['correct_answer'],
                        'explanation': q.get('explanation', ''),
                        'difficulty': q.get('difficulty', 'beginner'),
                    }
                )

            section_count = len(mod_data.get('sections', []))
            self.stdout.write(f'  ✓ {action} Module {mod_data["order"]}: {mod_data["title"]} ({section_count} sections)')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully! Start the server with:'))
        self.stdout.write('   python manage.py runserver')
