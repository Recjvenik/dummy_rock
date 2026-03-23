"""Seed glossary terms and learning paths."""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from modules.models import Module, GlossaryTerm, LearningPath

GLOSSARY_TERMS = [
    {'term': 'Algorithm', 'definition': 'A step-by-step set of instructions to solve a problem or perform a task.', 'simple_definition': 'A recipe that tells a computer exactly what to do, step by step.', 'example': 'A recipe for making tea is an algorithm — each step must be followed in order.', 'category': 'Basics', 'grade_level': '8'},
    {'term': 'Artificial Intelligence', 'definition': 'The simulation of human intelligence processes by computer systems, including learning, reasoning, and self-correction.', 'simple_definition': 'Making computers smart enough to do things that normally need human brains.', 'example': 'Siri understanding your voice commands is AI in action.', 'category': 'Basics', 'grade_level': '8'},
    {'term': 'Binary', 'definition': 'A number system that uses only two digits: 0 and 1. All computer data is stored in binary.', 'simple_definition': 'The language of computers — everything is stored as 0s and 1s.', 'example': 'The number 5 in binary is 101.', 'category': 'Basics', 'grade_level': '8'},
    {'term': 'Bit', 'definition': 'The smallest unit of data in computing, representing a single 0 or 1.', 'simple_definition': 'A single 0 or 1 — the tiniest piece of computer data.', 'example': '8 bits make 1 byte, which can store one character like "A".', 'category': 'Basics', 'grade_level': '8'},
    {'term': 'Neural Network', 'definition': 'A computing system inspired by biological neural networks, consisting of interconnected nodes (neurons) organized in layers that process information.', 'simple_definition': 'A computer system that tries to work like the human brain, with connected "neurons" that learn from examples.', 'example': 'Google Photos uses neural networks to recognize faces in your pictures.', 'category': 'ML', 'grade_level': '9'},
    {'term': 'Training Data', 'definition': 'The dataset used to train a machine learning model, from which the model learns patterns and relationships.', 'simple_definition': 'The examples you show to an AI so it can learn — like a textbook for machines.', 'example': 'To teach AI to recognize cats, you show it thousands of cat photos as training data.', 'category': 'ML', 'grade_level': '9'},
    {'term': 'Machine Learning', 'definition': 'A subset of AI where systems learn and improve from experience without being explicitly programmed for every scenario.', 'simple_definition': 'Teaching computers to learn from examples instead of giving them every single rule.', 'example': 'YouTube recommends videos by learning what you like to watch.', 'category': 'ML', 'grade_level': '9'},
    {'term': 'Deep Learning', 'definition': 'A subset of machine learning using neural networks with many layers to learn complex patterns from large datasets.', 'simple_definition': 'A type of AI that uses many layers of "brain-like" networks to understand really complex things like images and speech.', 'example': 'The AI that translates languages in real-time uses deep learning.', 'category': 'DL', 'grade_level': '10'},
    {'term': 'Dataset', 'definition': 'A structured collection of data used for analysis, training, or testing machine learning models.', 'simple_definition': 'A collection of organized information that AI uses to learn from.', 'example': 'A spreadsheet with 10,000 student records (marks, attendance, grade) is a dataset.', 'category': 'Basics', 'grade_level': '8'},
    {'term': 'Feature', 'definition': 'An individual measurable property or characteristic of a data point used as input to a machine learning model.', 'simple_definition': 'A single piece of information about something — like height, weight, or color.', 'example': 'To predict house prices, features might be: number of rooms, area, location.', 'category': 'ML', 'grade_level': '9'},
    {'term': 'Label', 'definition': 'The target output or answer in supervised learning that the model is trained to predict.', 'simple_definition': 'The correct answer that you give to AI during training so it knows what to learn.', 'example': 'In a spam filter, the label is "spam" or "not spam" for each email.', 'category': 'ML', 'grade_level': '9'},
    {'term': 'Model', 'definition': 'A mathematical representation learned from data that can make predictions or decisions on new, unseen data.', 'simple_definition': 'The "brain" that AI builds after learning from data — it can then make predictions on new things.', 'example': 'A weather prediction model takes today\'s data and predicts tomorrow\'s weather.', 'category': 'ML', 'grade_level': '9'},
    {'term': 'Overfitting', 'definition': 'When a model learns the training data too well, including noise and outliers, performing poorly on unseen data.', 'simple_definition': 'When AI memorizes the answers instead of actually learning — like mugging up a textbook without understanding.', 'example': 'A student who memorizes answers but can\'t solve new problems is overfitting!', 'category': 'ML', 'grade_level': '10'},
    {'term': 'Accuracy', 'definition': 'The percentage of correct predictions made by a model out of all predictions.', 'simple_definition': 'How often the AI gets the right answer — like scoring on a test.', 'example': 'If an AI correctly identifies 95 out of 100 images, its accuracy is 95%.', 'category': 'ML', 'grade_level': '9'},
    {'term': 'GPU', 'definition': 'Graphics Processing Unit — a specialized processor originally for graphics but now widely used for AI computations due to parallel processing capability.', 'simple_definition': 'A super-fast computer chip that can do many calculations at once — perfect for training AI.', 'example': 'NVIDIA GPUs are used to train ChatGPT and other large AI models.', 'category': 'Basics', 'grade_level': '10'},
    {'term': 'Transformer', 'definition': 'A neural network architecture based on self-attention mechanisms, introduced in 2017, forming the basis of modern LLMs.', 'simple_definition': 'The clever design behind ChatGPT and other language AIs — it helps AI understand how words relate to each other.', 'example': 'GPT stands for "Generative Pre-trained Transformer".', 'category': 'GenAI', 'grade_level': '11'},
    {'term': 'Tokenization', 'definition': 'The process of breaking text into smaller units (tokens) that a language model can process.', 'simple_definition': 'Chopping text into small pieces so AI can read it — like breaking a sentence into words or word-parts.', 'example': '"unbelievable" might be split into 3 tokens: "un", "believ", "able".', 'category': 'GenAI', 'grade_level': '11'},
    {'term': 'RAG', 'definition': 'Retrieval-Augmented Generation — a technique that combines information retrieval with LLM generation to provide accurate, source-grounded answers.', 'simple_definition': 'A technique where AI first looks up relevant information (like a student checking notes) before answering a question.', 'example': 'A customer service AI that looks up your order details before answering your question uses RAG.', 'category': 'GenAI', 'grade_level': '11'},
    {'term': 'Prompt', 'definition': 'The input text or instruction given to an AI model to generate a desired output.', 'simple_definition': 'The question or instruction you type to tell AI what you want — like giving directions.', 'example': '"Write a poem about rain" is a prompt for ChatGPT.', 'category': 'GenAI', 'grade_level': '10'},
    {'term': 'Hallucination', 'definition': 'When an AI model generates plausible-sounding but factually incorrect or fabricated information.', 'simple_definition': 'When AI makes up facts that sound real but are actually wrong — like a confident friend giving wrong directions.', 'example': 'An AI saying "The Eiffel Tower was built in 1920" when it was actually built in 1889.', 'category': 'GenAI', 'grade_level': '10'},
    {'term': 'Epoch', 'definition': 'One complete pass through the entire training dataset during model training.', 'simple_definition': 'Going through ALL the training examples once — like reading your entire textbook once.', 'example': 'Training for 100 epochs means the AI reviews all examples 100 times.', 'category': 'ML', 'grade_level': '10'},
    {'term': 'Gradient Descent', 'definition': 'An optimization algorithm that iteratively adjusts model parameters to minimize the loss function.', 'simple_definition': 'A technique where AI slowly adjusts itself to make fewer mistakes — like finding your way downhill in fog.', 'example': 'Imagine being blindfolded on a hill — you feel which way slopes down and take small steps that direction.', 'category': 'ML', 'grade_level': '11'},
    {'term': 'Loss Function', 'definition': 'A function that measures how far the model\'s predictions are from the actual values.', 'simple_definition': 'A score that tells the AI how wrong it was — lower is better, like golf.', 'example': 'If AI predicts temperature as 30°C but actual is 32°C, the loss might be (32-30)² = 4.', 'category': 'ML', 'grade_level': '11'},
    {'term': 'API', 'definition': 'Application Programming Interface — a set of rules and protocols that allow different software applications to communicate with each other.', 'simple_definition': 'A way for two computer programs to talk to each other — like a waiter taking orders between you and the kitchen.', 'example': 'When an app shows weather data, it uses a weather API to get the information.', 'category': 'Basics', 'grade_level': '10'},
    {'term': 'Chatbot', 'definition': 'An AI program designed to simulate conversation with users through text or voice.', 'simple_definition': 'A computer program you can chat with — like talking to a smart robot that understands language.', 'example': 'Customer service bots on websites that help answer your questions are chatbots.', 'category': 'GenAI', 'grade_level': '8'},
]

LEARNING_PATHS = [
    {'grade': '8', 'title': 'AI Explorer', 'description': 'Start your AI journey! Learn how computers work, what data means, and get your first taste of artificial intelligence.', 'estimated_duration': 20, 'icon': '🚀',
     'module_slugs': ['how-computers-think', 'data-patterns', 'ai-basics', 'ai-in-the-real-world']},
    {'grade': '9', 'title': 'AI Apprentice', 'description': 'Build your skills! Learn programming logic, understand patterns, and start thinking like a data scientist.', 'estimated_duration': 35, 'icon': '🔧',
     'module_slugs': ['how-computers-think', 'data-patterns', 'introduction-to-programming-logic', 'ai-basics', 'ai-in-the-real-world']},
    {'grade': '10', 'title': 'AI Builder', 'description': 'Get hands-on! Learn the math behind AI, build your first model, and understand how AI systems work end-to-end.', 'estimated_duration': 50, 'icon': '🏗️',
     'module_slugs': ['data-patterns', 'introduction-to-programming-logic', 'math-for-ai', 'ai-basics', 'building-your-first-model', 'machine-learning-deep-dive', 'ai-in-the-real-world']},
    {'grade': '11', 'title': 'AI Engineer', 'description': 'Go deeper! Master machine learning, deep learning, and generative AI concepts. Start building real AI applications.', 'estimated_duration': 80, 'icon': '⚙️',
     'module_slugs': ['math-for-ai', 'ai-basics', 'machine-learning-deep-dive', 'deep-learning-lab', 'generative-ai', 'building-your-first-model']},
    {'grade': '12', 'title': 'AI Architect', 'description': 'Master-level! Design production AI systems, understand LLM architectures, agents, and AI at scale.', 'estimated_duration': 120, 'icon': '🎓',
     'module_slugs': ['machine-learning-deep-dive', 'deep-learning-lab', 'generative-ai', 'llm-systems', 'agentic-ai', 'ai-playground']},
]


class Command(BaseCommand):
    help = 'Seed glossary terms and learning paths'

    def handle(self, *args, **kwargs):
        self.stdout.write('📖 Seeding Glossary Terms...')

        for term_data in GLOSSARY_TERMS:
            term, created = GlossaryTerm.objects.update_or_create(
                term=term_data['term'],
                defaults={
                    'definition': term_data['definition'],
                    'simple_definition': term_data['simple_definition'],
                    'example': term_data.get('example', ''),
                    'grade_level': term_data.get('grade_level', 'all'),
                    'category': term_data.get('category', ''),
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created term: {term_data["term"]}')
        self.stdout.write(f'  ✓ {len(GLOSSARY_TERMS)} glossary terms ensured')

        self.stdout.write('\n🗺️ Seeding Learning Paths...')
        for path_data in LEARNING_PATHS:
            path, created = LearningPath.objects.update_or_create(
                grade=path_data['grade'],
                defaults={
                    'title': path_data['title'],
                    'description': path_data['description'],
                    'estimated_duration': path_data['estimated_duration'],
                    'icon': path_data['icon'],
                }
            )
            # Link modules
            path.modules.clear()
            for slug in path_data.get('module_slugs', []):
                try:
                    module = Module.objects.get(slug=slug)
                    path.modules.add(module)
                except Module.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'    ⚠ Module not found: {slug}'))
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  ✓ {action} Path: Class {path_data["grade"]} — {path_data["title"]}')

        self.stdout.write(self.style.SUCCESS('\n✅ Glossary and Learning Paths seeded!'))
