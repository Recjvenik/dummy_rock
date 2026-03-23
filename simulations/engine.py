import math
import random
import time
from .models import SimulationLog


def log_simulation(user, sim_type, params, result, latency, tokens, cost, session_id=''):
    SimulationLog.objects.create(
        user=user if (user and user.is_authenticated) else None,
        simulation_type=sim_type,
        parameters=params,
        result=result,
        simulated_latency_ms=latency,
        simulated_tokens=tokens,
        simulated_cost_usd=cost,
        session_id=session_id,
    )


# ─── Neural Network Simulator ─────────────────────────────────────────────────
def simulate_neural_network(params: dict) -> dict:
    """Generate neural network layer data for visualization"""
    layers = params.get('layers', [4, 8, 6, 2])
    activation = params.get('activation', 'relu')

    def activation_fn(x):
        if activation == 'relu':
            return max(0, x)
        elif activation == 'sigmoid':
            return 1 / (1 + math.exp(-x))
        elif activation == 'tanh':
            return math.tanh(x)
        return x  # linear

    network_data = []
    for i, size in enumerate(layers):
        layer_type = 'input' if i == 0 else ('output' if i == len(layers) - 1 else 'hidden')
        neurons = []
        for j in range(size):
            val = random.uniform(-1, 1)
            neurons.append({
                'id': f'L{i}N{j}',
                'value': round(activation_fn(val), 4),
                'raw': round(val, 4),
            })
        network_data.append({'layer_index': i, 'layer_type': layer_type, 'neurons': neurons})

    # Generate weights
    weights = []
    for i in range(len(layers) - 1):
        for src in range(layers[i]):
            for dst in range(layers[i + 1]):
                weights.append({
                    'from': f'L{i}N{src}',
                    'to': f'L{i+1}N{dst}',
                    'weight': round(random.uniform(-1, 1), 3),
                })

    # Calculate network statistics
    total_params = sum(
        layers[i] * layers[i + 1] + layers[i + 1]  # weights + biases
        for i in range(len(layers) - 1)
    )
    total_neurons = sum(layers)

    return {
        'layers': network_data,
        'weights': weights,
        'activation': activation,
        'total_params': total_params,
        'total_neurons': total_neurons,
        'layer_sizes': layers,
    }


# ─── Gradient Descent Simulator ───────────────────────────────────────────────
def simulate_gradient_descent(params: dict) -> dict:
    learning_rate = float(params.get('learning_rate', 0.1))
    epochs = int(params.get('epochs', 50))
    start_x = float(params.get('start_x', 5.0))

    # Simple f(x) = x^2 + 2x + 1 → minimum at x = -1
    def f(x): return x ** 2 + 2 * x + 1
    def df(x): return 2 * x + 2  # derivative

    x = start_x
    path = []
    for i in range(epochs):
        loss = f(x)
        grad = df(x)
        path.append({'epoch': i, 'x': round(x, 4), 'loss': round(loss, 4), 'gradient': round(grad, 4)})
        x = x - learning_rate * grad
        if abs(grad) < 1e-6:
            break

    return {
        'path': path,
        'final_x': round(x, 4),
        'final_loss': round(f(x), 4),
        'minimum_x': -1.0,
        'converged': abs(x - (-1.0)) < 0.01,
    }


# ─── Activation Function Visualizer ──────────────────────────────────────────
def simulate_activation_functions(params: dict) -> dict:
    x_values = [round(-5 + i * 0.2, 1) for i in range(51)]
    functions = {
        'relu': [max(0, x) for x in x_values],
        'sigmoid': [round(1 / (1 + math.exp(-x)), 4) for x in x_values],
        'tanh': [round(math.tanh(x), 4) for x in x_values],
        'leaky_relu': [round(x if x > 0 else 0.01 * x, 4) for x in x_values],
        'linear': [round(x, 4) for x in x_values],
    }
    return {'x_values': x_values, 'functions': functions}


# ─── Bias-Variance Simulator ──────────────────────────────────────────────────
def simulate_bias_variance(params: dict) -> dict:
    model_complexity = int(params.get('complexity', 5))  # 1-10
    noise_level = float(params.get('noise', 0.3))
    n_points = 50

    # True function: sin(x)
    x = [round(i * 0.2, 2) for i in range(n_points)]
    true_y = [round(math.sin(xi), 3) for xi in x]
    noisy_y = [round(math.sin(xi) + random.gauss(0, noise_level), 3) for xi in x]

    # Simple polynomial approximation
    bias = max(0, 1 - model_complexity / 10)
    variance = min(1, model_complexity / 10)
    total_error = round(bias ** 2 + variance + noise_level ** 2, 4)

    return {
        'x': x,
        'true_y': true_y,
        'noisy_y': noisy_y,
        'bias': round(bias, 3),
        'variance': round(variance, 3),
        'irreducible_error': round(noise_level ** 2, 3),
        'total_error': total_error,
        'overfitting': model_complexity > 7,
        'underfitting': model_complexity < 3,
    }


# ─── LLM Parameter Simulator ──────────────────────────────────────────────────
def simulate_llm_params(params: dict) -> dict:
    temperature = float(params.get('temperature', 0.7))
    top_k = int(params.get('top_k', 50))
    top_p = float(params.get('top_p', 0.9))
    model_size = params.get('model_size', '7B')
    chunk_size = int(params.get('chunk_size', 512))
    reranking = params.get('reranking', False)

    model_latency_map = {'3B': 200, '7B': 450, '13B': 900, '70B': 3500, 'claude-opus': 2800}
    base_latency = model_latency_map.get(model_size, 500)

    # Simulated metrics
    latency_ms = base_latency * (1 + temperature * 0.2) + (100 if reranking else 0)
    token_cost_per_1k = {'3B': 0.001, '7B': 0.002, '13B': 0.004, '70B': 0.01, 'claude-opus': 0.015}
    cost_per_1k = token_cost_per_1k.get(model_size, 0.005)
    estimated_tokens = random.randint(200, 800)
    cost = round((estimated_tokens / 1000) * cost_per_1k, 6)

    # Hallucination risk (high temp = more creative but riskier)
    hall_risk = min(100, int(temperature * 60 + (1 - top_p) * 20))
    accuracy = max(20, int(100 - hall_risk * 0.5 - (model_size == '3B') * 20))

    return {
        'latency_ms': round(latency_ms, 1),
        'estimated_tokens': estimated_tokens,
        'cost_usd': cost,
        'hallucination_risk_pct': hall_risk,
        'accuracy_pct': accuracy,
        'diversity_score': min(100, int(temperature * 80 + top_k * 0.4)),
        'chunk_size': chunk_size,
        'reranking_enabled': reranking,
    }


# ─── RAG Pipeline Simulator ───────────────────────────────────────────────────
def simulate_rag_pipeline(params: dict) -> dict:
    query = params.get('query', 'What is Retrieval Augmented Generation?')
    chunk_size = int(params.get('chunk_size', 512))
    top_k = int(params.get('top_k', 5))
    reranking = params.get('reranking', True)
    embedding_model = params.get('embedding_model', 'text-embedding-ada-002')

    stages = [
        {'stage': 'User Query', 'latency_ms': 0, 'tokens': len(query.split()),
         'description': f'Query received: "{query[:50]}..."'},
        {'stage': 'Chunking', 'latency_ms': random.randint(5, 20), 'tokens': 0,
         'description': f'Document split into chunks of {chunk_size} tokens'},
        {'stage': 'Embedding', 'latency_ms': random.randint(50, 150), 'tokens': len(query.split()),
         'description': f'Query embedded using {embedding_model}'},
        {'stage': 'Vector Search', 'latency_ms': random.randint(30, 100), 'tokens': 0,
         'description': f'Retrieved top-{top_k} similar chunks from vector DB'},
        {'stage': 'Re-ranking' if reranking else 'Skip Re-rank',
         'latency_ms': random.randint(80, 200) if reranking else 0, 'tokens': 0,
         'description': 'Cross-encoder re-ranking applied' if reranking else 'Re-ranking skipped'},
        {'stage': 'LLM Generation', 'latency_ms': random.randint(800, 2500),
         'tokens': random.randint(300, 700),
         'description': 'Claude generating response from context'},
        {'stage': 'Response', 'latency_ms': 0, 'tokens': 0,
         'description': 'Final answer delivered to user'},
    ]

    total_latency = sum(s['latency_ms'] for s in stages)
    total_tokens = sum(s['tokens'] for s in stages)

    # Fake retrieved chunks
    retrieved_chunks = [
        {
            'id': f'chunk_{i}',
            'score': round(random.uniform(0.6, 0.99), 3),
            'text': f'Relevant document chunk {i+1} about {query[:30]}...',
            'source': f'document_{random.randint(1, 20)}.pdf',
        }
        for i in range(top_k)
    ]
    retrieved_chunks.sort(key=lambda x: x['score'], reverse=True)

    return {
        'stages': stages,
        'total_latency_ms': total_latency,
        'total_tokens': total_tokens,
        'cost_usd': round(total_tokens / 1000 * 0.015, 6),
        'retrieved_chunks': retrieved_chunks,
    }


# ─── Agent Flow Simulator ──────────────────────────────────────────────────────
def simulate_agent_flow(params: dict) -> dict:
    task = params.get('task', 'Research the latest AI papers and summarize key findings')
    agent_type = params.get('agent_type', 'ReAct')
    tools = params.get('tools', ['search', 'calculator', 'code_executor'])
    memory_enabled = params.get('memory', True)
    max_iterations = int(params.get('max_iterations', 5))

    steps = [
        {'step': 'Task Received', 'agent': 'Orchestrator', 'action': 'parse_task',
         'thought': f'Analyzing task: "{task[:60]}..."', 'tool': None,
         'latency_ms': random.randint(100, 300), 'tokens': 50},
        {'step': 'Planning', 'agent': 'Planner', 'action': 'decompose_task',
         'thought': 'Breaking down task into subtasks', 'tool': None,
         'latency_ms': random.randint(500, 1200), 'tokens': 200},
    ]

    for i in range(min(max_iterations, 3)):
        tool = random.choice(tools)
        steps.append({
            'step': f'Iteration {i+1}',
            'agent': 'Executor',
            'action': f'call_tool_{tool}',
            'thought': f'Using {tool} to gather information',
            'tool': tool,
            'tool_result': f'Result from {tool}: [simulated data]',
            'latency_ms': random.randint(200, 800),
            'tokens': random.randint(100, 400),
        })

    if memory_enabled:
        steps.append({
            'step': 'Memory Update', 'agent': 'Memory Manager',
            'action': 'store_context', 'thought': 'Storing relevant context to memory',
            'tool': 'memory_store', 'latency_ms': random.randint(20, 80), 'tokens': 50,
        })

    steps.append({
        'step': 'Reflection', 'agent': 'Critic', 'action': 'evaluate_result',
        'thought': 'Evaluating quality and completeness of answer',
        'tool': None, 'latency_ms': random.randint(300, 700), 'tokens': 150,
    })

    steps.append({
        'step': 'Final Output', 'agent': 'Orchestrator', 'action': 'format_response',
        'thought': 'Formatting and returning final answer to user',
        'tool': None, 'latency_ms': random.randint(100, 300), 'tokens': 300,
    })

    total_latency = sum(s['latency_ms'] for s in steps)
    total_tokens = sum(s['tokens'] for s in steps)

    return {
        'steps': steps,
        'agent_type': agent_type,
        'total_latency_ms': total_latency,
        'total_tokens': total_tokens,
        'cost_usd': round(total_tokens / 1000 * 0.015, 6),
        'tools_used': list(set(s['tool'] for s in steps if s.get('tool'))),
        'memory_enabled': memory_enabled,
    }


# ─── Tokenizer Visualizer ──────────────────────────────────────────────────────
def simulate_tokenizer(params: dict) -> dict:
    text = params.get('text', 'Hello, how are you doing today?')
    tokenizer_type = params.get('tokenizer', 'BPE')

    # Naive word-level tokenization for demo
    words = text.split()
    tokens = []
    colors = ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff', '#ff6bca', '#b15eff']
    for i, word in enumerate(words):
        tokens.append({
            'token': word,
            'token_id': hash(word) % 50000,
            'color': colors[i % len(colors)],
            'bytes': len(word.encode('utf-8')),
        })

    return {
        'original_text': text,
        'tokens': tokens,
        'token_count': len(tokens),
        'character_count': len(text),
        'tokenizer_type': tokenizer_type,
        'compression_ratio': round(len(text) / max(len(tokens), 1), 2),
    }


# ─── Logic Gates Simulator (Class 8-9) ────────────────────────────────────────
def simulate_logic_gates(params: dict) -> dict:
    gate_type = params.get('gate', 'AND').upper()
    input_a = int(params.get('input_a', 0))
    input_b = int(params.get('input_b', 0))

    gates = {
        'AND':  {'truth': [[0,0,0],[0,1,0],[1,0,0],[1,1,1]], 'desc': 'Both inputs must be 1'},
        'OR':   {'truth': [[0,0,0],[0,1,1],[1,0,1],[1,1,1]], 'desc': 'At least one input must be 1'},
        'NOT':  {'truth': [[0,1],[1,0]], 'desc': 'Flips the input'},
        'XOR':  {'truth': [[0,0,0],[0,1,1],[1,0,1],[1,1,0]], 'desc': 'Exactly one input must be 1'},
        'NAND': {'truth': [[0,0,1],[0,1,1],[1,0,1],[1,1,0]], 'desc': 'NOT of AND — output 0 only when both are 1'},
    }

    gate_info = gates.get(gate_type, gates['AND'])

    if gate_type == 'NOT':
        output = 1 - input_a
    elif gate_type == 'AND':
        output = input_a & input_b
    elif gate_type == 'OR':
        output = input_a | input_b
    elif gate_type == 'XOR':
        output = input_a ^ input_b
    elif gate_type == 'NAND':
        output = 1 - (input_a & input_b)
    else:
        output = 0

    return {
        'gate': gate_type,
        'input_a': input_a,
        'input_b': input_b,
        'output': output,
        'truth_table': gate_info['truth'],
        'description': gate_info['desc'],
        'all_gates': list(gates.keys()),
    }


# ─── Data Sorting Visualizer (Class 8-9) ──────────────────────────────────────
def simulate_data_sorting(params: dict) -> dict:
    data = params.get('data', [64, 34, 25, 12, 22, 11, 90])
    algorithm = params.get('algorithm', 'bubble').lower()

    arr = list(data)
    steps = [{'step': 0, 'array': list(arr), 'action': 'Initial array', 'comparing': []}]

    if algorithm == 'bubble':
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                comparing = [j, j + 1]
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    steps.append({
                        'step': len(steps),
                        'array': list(arr),
                        'action': f'Swap {arr[j+1]} and {arr[j]}',
                        'comparing': comparing,
                        'swapped': True,
                    })
                else:
                    steps.append({
                        'step': len(steps),
                        'array': list(arr),
                        'action': f'{arr[j]} ≤ {arr[j+1]}, no swap',
                        'comparing': comparing,
                        'swapped': False,
                    })
    elif algorithm == 'selection':
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({
                'step': len(steps),
                'array': list(arr),
                'action': f'Place {arr[i]} at position {i}',
                'comparing': [i, min_idx],
                'swapped': i != min_idx,
            })

    return {
        'algorithm': algorithm,
        'original': list(data),
        'sorted': list(arr),
        'steps': steps[:30],  # cap at 30 steps for display
        'total_steps': len(steps),
        'is_sorted': arr == sorted(data),
    }


# ─── Pattern Recognition Exercise (Class 8-9) ─────────────────────────────────
def simulate_pattern_recognition(params: dict) -> dict:
    pattern_type = params.get('type', 'number')

    patterns = {
        'number': [
            {'sequence': [2, 4, 6, 8], 'answer': 10, 'rule': 'Add 2 each time'},
            {'sequence': [1, 4, 9, 16], 'answer': 25, 'rule': 'Square numbers: 1², 2², 3², 4², 5²'},
            {'sequence': [1, 1, 2, 3, 5], 'answer': 8, 'rule': 'Fibonacci: each number = sum of previous two'},
            {'sequence': [3, 6, 12, 24], 'answer': 48, 'rule': 'Multiply by 2 each time'},
            {'sequence': [100, 90, 80, 70], 'answer': 60, 'rule': 'Subtract 10 each time'},
        ],
        'letter': [
            {'sequence': ['A', 'C', 'E', 'G'], 'answer': 'I', 'rule': 'Skip one letter each time'},
            {'sequence': ['Z', 'Y', 'X', 'W'], 'answer': 'V', 'rule': 'Reverse alphabet'},
        ],
    }

    selected = patterns.get(pattern_type, patterns['number'])
    challenge = random.choice(selected)

    return {
        'pattern_type': pattern_type,
        'sequence': challenge['sequence'],
        'correct_answer': challenge['answer'],
        'rule': challenge['rule'],
        'hint': f'Look at the difference between consecutive elements',
        'available_types': list(patterns.keys()),
    }


# ─── K-Means Clustering Simulator ─────────────────────────────────────────────

def simulate_kmeans(params: dict) -> dict:
    """Interactive K-Means clustering simulator with step-by-step iterations."""
    n_points = max(20, min(int(params.get('n_points', 80)), 300))
    n_clusters = max(2, min(int(params.get('n_clusters', 3)), 8))
    max_iterations = max(3, min(int(params.get('max_iterations', 20)), 50))
    seed = int(params.get('seed', 42))

    rng = random.Random(seed)

    # Generate clustered data
    true_centers = [(rng.uniform(0.1, 0.9), rng.uniform(0.1, 0.9)) for _ in range(n_clusters)]
    points = []
    for i in range(n_points):
        cx, cy = true_centers[i % n_clusters]
        x = max(0.0, min(1.0, cx + rng.gauss(0, 0.12)))
        y = max(0.0, min(1.0, cy + rng.gauss(0, 0.12)))
        points.append({'x': round(x, 4), 'y': round(y, 4)})

    # Initialize centroids randomly
    init_method = params.get('init_method', 'random')
    if init_method == 'kmeans++':
        centroids = [points[rng.randint(0, n_points - 1)].copy()]
        for _ in range(n_clusters - 1):
            dists = []
            for p in points:
                min_d = min((p['x']-c['x'])**2 + (p['y']-c['y'])**2 for c in centroids)
                dists.append(min_d)
            total = sum(dists)
            r = rng.random() * total
            cumsum = 0
            for i, d in enumerate(dists):
                cumsum += d
                if cumsum >= r:
                    centroids.append({'x': points[i]['x'], 'y': points[i]['y']})
                    break
    else:
        chosen = rng.sample(range(n_points), n_clusters)
        centroids = [{'x': points[i]['x'], 'y': points[i]['y']} for i in chosen]

    iterations = []
    prev_assignments = None

    for iteration in range(max_iterations):
        # Assign points to nearest centroid
        assignments = []
        for p in points:
            dists = [math.sqrt((p['x'] - c['x'])**2 + (p['y'] - c['y'])**2) for c in centroids]
            assignments.append(dists.index(min(dists)))

        # Compute inertia
        inertia = sum(
            (points[i]['x'] - centroids[assignments[i]]['x'])**2 +
            (points[i]['y'] - centroids[assignments[i]]['y'])**2
            for i in range(n_points)
        )

        iterations.append({
            'step': iteration + 1,
            'centroids': [{'x': round(c['x'], 4), 'y': round(c['y'], 4), 'cluster_id': j}
                          for j, c in enumerate(centroids)],
            'assignments': assignments[:],
            'inertia': round(inertia, 6),
        })

        if assignments == prev_assignments:
            break
        prev_assignments = assignments[:]

        # Update centroids
        for k in range(n_clusters):
            cluster_pts = [points[i] for i, a in enumerate(assignments) if a == k]
            if cluster_pts:
                centroids[k] = {
                    'x': round(sum(p['x'] for p in cluster_pts) / len(cluster_pts), 4),
                    'y': round(sum(p['y'] for p in cluster_pts) / len(cluster_pts), 4),
                }

    converged = len(iterations) < max_iterations
    return {
        'points': points,
        'iterations': iterations,
        'final_clusters': n_clusters,
        'converged': converged,
        'total_iterations': len(iterations),
        'init_method': init_method,
    }


# ─── Decision Tree Simulator ───────────────────────────────────────────────────

def _gini(labels):
    if not labels:
        return 0.0
    n = len(labels)
    counts = {}
    for l in labels:
        counts[l] = counts.get(l, 0) + 1
    return 1.0 - sum((c / n) ** 2 for c in counts.values())


def _entropy(labels):
    if not labels:
        return 0.0
    n = len(labels)
    counts = {}
    for l in labels:
        counts[l] = counts.get(l, 0) + 1
    result = 0.0
    for c in counts.values():
        p = c / n
        if p > 0:
            result -= p * math.log2(p)
    return result


def _majority(labels):
    counts = {}
    for l in labels:
        counts[l] = counts.get(l, 0) + 1
    return max(counts, key=counts.get)


def _build_tree(X, y, feature_names, class_names, criterion_fn, depth, max_depth, min_samples, node_id_counter):
    node_id = node_id_counter[0]
    node_id_counter[0] += 1
    n = len(y)

    counts = {}
    for label in y:
        counts[label] = counts.get(label, 0) + 1
    impurity = criterion_fn(y)

    if depth >= max_depth or n < min_samples or len(set(y)) == 1:
        return {
            'node_id': node_id, 'is_leaf': True, 'class_label': _majority(y),
            'samples': n, 'gini': round(impurity, 4), 'value': counts,
            'feature': None, 'threshold': None, 'left': None, 'right': None,
        }

    best_feature, best_threshold, best_impurity = None, None, float('inf')
    n_features = len(feature_names)

    for fi in range(n_features):
        vals = sorted(set(row[fi] for row in X))
        for i in range(len(vals) - 1):
            thresh = (vals[i] + vals[i + 1]) / 2.0
            left_y = [y[j] for j, row in enumerate(X) if row[fi] <= thresh]
            right_y = [y[j] for j, row in enumerate(X) if row[fi] > thresh]
            if not left_y or not right_y:
                continue
            imp = (len(left_y) * criterion_fn(left_y) + len(right_y) * criterion_fn(right_y)) / n
            if imp < best_impurity:
                best_impurity = imp
                best_feature = fi
                best_threshold = thresh

    if best_feature is None:
        return {
            'node_id': node_id, 'is_leaf': True, 'class_label': _majority(y),
            'samples': n, 'gini': round(impurity, 4), 'value': counts,
            'feature': None, 'threshold': None, 'left': None, 'right': None,
        }

    left_mask = [row[best_feature] <= best_threshold for row in X]
    left_X = [X[i] for i, m in enumerate(left_mask) if m]
    left_y = [y[i] for i, m in enumerate(left_mask) if m]
    right_X = [X[i] for i, m in enumerate(left_mask) if not m]
    right_y = [y[i] for i, m in enumerate(left_mask) if not m]

    return {
        'node_id': node_id, 'is_leaf': False,
        'feature': feature_names[best_feature],
        'feature_idx': best_feature,
        'threshold': round(best_threshold, 3),
        'samples': n, 'gini': round(impurity, 4),
        'class_label': _majority(y), 'value': counts,
        'left': _build_tree(left_X, left_y, feature_names, class_names, criterion_fn, depth + 1, max_depth, min_samples, node_id_counter),
        'right': _build_tree(right_X, right_y, feature_names, class_names, criterion_fn, depth + 1, max_depth, min_samples, node_id_counter),
    }


def simulate_decision_tree(params: dict) -> dict:
    """Decision tree builder with Gini/Entropy splitting."""
    max_depth = max(1, min(int(params.get('max_depth', 3)), 6))
    min_samples = max(2, min(int(params.get('min_samples', 5)), 30))
    criterion = params.get('criterion', 'gini')
    seed = int(params.get('seed', 42))
    rng = random.Random(seed)

    # Generate synthetic 2-class dataset
    n = 100
    X, y = [], []
    for _ in range(n):
        x1 = rng.uniform(0, 10)
        x2 = rng.uniform(0, 10)
        # Non-linear boundary
        label = 1 if (x1 - 5) ** 2 + (x2 - 5) ** 2 < 9 + rng.gauss(0, 1) else 0
        X.append([round(x1, 2), round(x2, 2)])
        y.append(label)

    feature_names = ['Feature A', 'Feature B']
    class_names = ['Class 0', 'Class 1']
    criterion_fn = _gini if criterion == 'gini' else _entropy

    tree = _build_tree(X, y, feature_names, class_names, criterion_fn, 0, max_depth, min_samples, [0])

    # Calculate accuracy
    def predict(node, x):
        if node['is_leaf']:
            return node['class_label']
        if x[node['feature_idx']] <= node['threshold']:
            return predict(node['left'], x)
        return predict(node['right'], x)

    correct = sum(1 for i, xi in enumerate(X) if predict(tree, xi) == y[i])
    accuracy = round(correct / n * 100, 1)

    def tree_depth(node):
        if node['is_leaf']:
            return 0
        return 1 + max(tree_depth(node['left']), tree_depth(node['right']))

    return {
        'tree': tree,
        'feature_names': feature_names,
        'class_names': class_names,
        'accuracy': accuracy,
        'depth': tree_depth(tree),
        'n_samples': n,
        'criterion': criterion,
        'dataset': [{'x1': X[i][0], 'x2': X[i][1], 'label': y[i]} for i in range(n)],
    }


# ─── Attention Mechanism Simulator ────────────────────────────────────────────

def _softmax(values, temperature=1.0):
    scaled = [v / temperature for v in values]
    max_v = max(scaled)
    exps = [math.exp(v - max_v) for v in scaled]
    total = sum(exps)
    return [e / total for e in exps]


def simulate_attention(params: dict) -> dict:
    """Self-attention mechanism visualizer."""
    text = params.get('sequence', 'The cat sat on the mat')
    temperature = max(0.1, min(float(params.get('temperature', 1.0)), 3.0))
    dim = 8
    seed = 42

    tokens = text.strip().split()[:12]
    n = len(tokens)
    if n < 2:
        tokens = ['The', 'quick', 'brown', 'fox']
        n = 4

    rng = random.Random(seed)

    def rand_vec(size):
        return [round(rng.gauss(0, 0.5), 3) for _ in range(size)]

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    # Generate Q, K, V vectors per token
    Q = [rand_vec(dim) for _ in range(n)]
    K = [rand_vec(dim) for _ in range(n)]
    V = [rand_vec(dim) for _ in range(n)]

    # Compute attention weights
    scale = math.sqrt(dim)
    attention_weights = []
    for i in range(n):
        scores = [dot(Q[i], K[j]) / scale for j in range(n)]
        weights = _softmax(scores, temperature)
        attention_weights.append([round(w, 4) for w in weights])

    # Compute output vectors (weighted sum of V)
    outputs = []
    for i in range(n):
        out = [0.0] * dim
        for j in range(n):
            for d in range(dim):
                out[d] += attention_weights[i][j] * V[j][d]
        outputs.append([round(v, 3) for v in out])

    # Top attending pairs
    top_attention = []
    for i in range(n):
        sorted_j = sorted(range(n), key=lambda j: attention_weights[i][j], reverse=True)
        top_attention.append({
            'token': tokens[i],
            'top_attends_to': [
                {'token': tokens[j], 'weight': attention_weights[i][j]}
                for j in sorted_j[:3]
            ]
        })

    return {
        'tokens': tokens,
        'attention_weights': attention_weights,
        'q_vectors': Q,
        'k_vectors': K,
        'v_vectors': V,
        'output_vectors': outputs,
        'temperature': temperature,
        'dim': dim,
        'top_attention': top_attention,
        'entropy': round(sum(-w * math.log2(w + 1e-9) for row in attention_weights for w in row) / n, 3),
    }

