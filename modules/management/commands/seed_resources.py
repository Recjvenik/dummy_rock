"""
Management command to seed curated learning resources for all AI Lab modules
Run with: python manage.py seed_resources
"""

from django.core.management.base import BaseCommand
from modules.models import Module, LearningResource


class Command(BaseCommand):
    help = 'Seeds curated learning resources (videos, articles, courses) for all modules'

    def handle(self, *args, **kwargs):
        self.stdout.write('🎓 Seeding Learning Resources...\n')
        
        # Clear existing resources
        LearningResource.objects.all().delete()
        
        resources_data = {
            'ai-basics': [
                {
                    'title': 'But what is a neural network? | Deep learning, chapter 1',
                    'resource_type': 'video',
                    'url': 'https://www.youtube.com/watch?v=aircAruvnKk',
                    'description': 'Visual introduction to neural networks by 3Blue1Brown. Perfect for beginners to understand the fundamentals.',
                    'author': '3Blue1Brown',
                    'duration': '19 min',
                    'difficulty': 'beginner',
                    'is_free': True,
                },
                {
                    'title': 'AI For Everyone - Coursera',
                    'resource_type': 'course',
                    'url': 'https://www.coursera.org/learn/ai-for-everyone',
                    'description': 'Non-technical course by Andrew Ng explaining AI concepts, applications, and impact.',
                    'author': 'Andrew Ng',
                    'duration': '6 hours',
                    'difficulty': 'beginner',
                    'is_free': True,
                },
                {
                    'title': 'Elements of AI - Free Online Course',
                    'resource_type': 'course',
                    'url': 'https://www.elementsofai.com/',
                    'description': 'Interactive course covering AI basics, machine learning, and neural networks.',
                    'author': 'University of Helsinki',
                    'duration': '30 hours',
                    'difficulty': 'beginner',
                    'is_free': True,
                },
                {
                    'title': 'Artificial Intelligence: A Modern Approach',
                    'resource_type': 'book',
                    'url': 'http://aima.cs.berkeley.edu/',
                    'description': 'The definitive textbook on AI. Comprehensive coverage of all AI topics.',
                    'author': 'Stuart Russell & Peter Norvig',
                    'duration': '1100 pages',
                    'difficulty': 'intermediate',
                    'is_free': False,
                },
            ],
            
            'machine-learning-deep-dive': [
                {
                    'title': 'Machine Learning Crash Course - Google',
                    'resource_type': 'course',
                    'url': 'https://developers.google.com/machine-learning/crash-course',
                    'description': 'Fast-paced, practical introduction to machine learning with TensorFlow APIs.',
                    'author': 'Google',
                    'duration': '15 hours',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
                {
                    'title': 'StatQuest: Machine Learning',
                    'resource_type': 'video',
                    'url': 'https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF',
                    'description': 'Clear, step-by-step explanations of ML algorithms with visual examples.',
                    'author': 'Josh Starmer',
                    'duration': '10+ hours',
                    'difficulty': 'beginner',
                    'is_free': True,
                },
                {
                    'title': 'Hands-On Machine Learning with Scikit-Learn and TensorFlow',
                    'resource_type': 'book',
                    'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/',
                    'description': 'Practical guide to building ML systems with real-world examples.',
                    'author': 'Aurélien Géron',
                    'duration': '850 pages',
                    'difficulty': 'intermediate',
                    'is_free': False,
                },
                {
                    'title': 'Machine Learning - Stanford CS229',
                    'resource_type': 'course',
                    'url': 'https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU',
                    'description': 'Complete Stanford course on machine learning theory and applications.',
                    'author': 'Andrew Ng',
                    'duration': '20 hours',
                    'difficulty': 'advanced',
                    'is_free': True,
                },
            ],
            
            'deep-learning-lab': [
                {
                    'title': 'Deep Learning Specialization - Coursera',
                    'resource_type': 'course',
                    'url': 'https://www.coursera.org/specializations/deep-learning',
                    'description': '5-course specialization covering neural networks, CNNs, RNNs, and more.',
                    'author': 'Andrew Ng',
                    'duration': '3 months',
                    'difficulty': 'intermediate',
                    'is_free': False,
                },
                {
                    'title': 'Neural Networks and Deep Learning',
                    'resource_type': 'book',
                    'url': 'http://neuralnetworksanddeeplearning.com/',
                    'description': 'Free online book explaining neural networks from first principles.',
                    'author': 'Michael Nielsen',
                    'duration': '200 pages',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
                {
                    'title': 'MIT 6.S191: Introduction to Deep Learning',
                    'resource_type': 'course',
                    'url': 'http://introtodeeplearning.com/',
                    'description': 'MIT course with lectures, labs, and projects on deep learning.',
                    'author': 'MIT',
                    'duration': '7 days',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
                {
                    'title': 'Deep Learning with PyTorch',
                    'resource_type': 'interactive',
                    'url': 'https://pytorch.org/tutorials/',
                    'description': 'Official PyTorch tutorials with hands-on examples and code.',
                    'author': 'PyTorch Team',
                    'duration': 'Self-paced',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
            ],
            
            'generative-ai': [
                {
                    'title': 'Introduction to Generative AI - Google Cloud',
                    'resource_type': 'course',
                    'url': 'https://www.cloudskillsboost.google/paths/118',
                    'description': 'Learn about generative AI, large language models, and responsible AI.',
                    'author': 'Google Cloud',
                    'duration': '10 hours',
                    'difficulty': 'beginner',
                    'is_free': True,
                },
                {
                    'title': 'Generative AI with Large Language Models',
                    'resource_type': 'course',
                    'url': 'https://www.coursera.org/learn/generative-ai-with-llms',
                    'description': 'Deep dive into LLM architecture, training, and fine-tuning.',
                    'author': 'DeepLearning.AI',
                    'duration': '16 hours',
                    'difficulty': 'intermediate',
                    'is_free': False,
                },
                {
                    'title': 'Attention Is All You Need - Original Transformer Paper',
                    'resource_type': 'paper',
                    'url': 'https://arxiv.org/abs/1706.03762',
                    'description': 'The groundbreaking paper that introduced the Transformer architecture.',
                    'author': 'Vaswani et al.',
                    'duration': '15 pages',
                    'difficulty': 'advanced',
                    'is_free': True,
                },
                {
                    'title': 'Hugging Face Course',
                    'resource_type': 'interactive',
                    'url': 'https://huggingface.co/learn/nlp-course',
                    'description': 'Learn to use transformers for NLP tasks with hands-on exercises.',
                    'author': 'Hugging Face',
                    'duration': '40 hours',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
            ],
            
            'llm-systems': [
                {
                    'title': 'Building LLM Applications - Full Stack Deep Learning',
                    'resource_type': 'course',
                    'url': 'https://fullstackdeeplearning.com/llm-bootcamp/',
                    'description': 'Practical course on building production LLM applications.',
                    'author': 'Full Stack Deep Learning',
                    'duration': '8 hours',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
                {
                    'title': 'LangChain Documentation',
                    'resource_type': 'documentation',
                    'url': 'https://python.langchain.com/docs/get_started/introduction',
                    'description': 'Official docs for building LLM applications with LangChain.',
                    'author': 'LangChain',
                    'duration': 'Reference',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
                {
                    'title': 'Prompt Engineering Guide',
                    'resource_type': 'article',
                    'url': 'https://www.promptingguide.ai/',
                    'description': 'Comprehensive guide to prompt engineering techniques and best practices.',
                    'author': 'DAIR.AI',
                    'duration': '2 hours',
                    'difficulty': 'beginner',
                    'is_free': True,
                },
                {
                    'title': 'RAG Systems: A Practical Guide',
                    'resource_type': 'article',
                    'url': 'https://www.pinecone.io/learn/retrieval-augmented-generation/',
                    'description': 'Learn how to build Retrieval-Augmented Generation systems.',
                    'author': 'Pinecone',
                    'duration': '30 min',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
            ],
            
            'agentic-ai': [
                {
                    'title': 'AI Agents - DeepLearning.AI',
                    'resource_type': 'course',
                    'url': 'https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/',
                    'description': 'Learn to build AI agents with memory, tools, and planning capabilities.',
                    'author': 'DeepLearning.AI',
                    'duration': '1 hour',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
                {
                    'title': 'ReAct: Synergizing Reasoning and Acting in Language Models',
                    'resource_type': 'paper',
                    'url': 'https://arxiv.org/abs/2210.03629',
                    'description': 'Research paper on the ReAct pattern for building reasoning agents.',
                    'author': 'Yao et al.',
                    'duration': '16 pages',
                    'difficulty': 'advanced',
                    'is_free': True,
                },
                {
                    'title': 'AutoGPT and Agent Architectures',
                    'resource_type': 'video',
                    'url': 'https://www.youtube.com/watch?v=jn8n212l3PQ',
                    'description': 'Understanding autonomous AI agents and their architectures.',
                    'author': 'AI Explained',
                    'duration': '25 min',
                    'difficulty': 'intermediate',
                    'is_free': True,
                },
                {
                    'title': 'LangGraph Documentation',
                    'resource_type': 'documentation',
                    'url': 'https://langchain-ai.github.io/langgraph/',
                    'description': 'Build stateful, multi-actor applications with LLMs.',
                    'author': 'LangChain',
                    'duration': 'Reference',
                    'difficulty': 'advanced',
                    'is_free': True,
                },
            ],
        }
        
        # Seed resources for each module
        for module_slug, resources in resources_data.items():
            try:
                module = Module.objects.get(slug=module_slug)
                for idx, resource_data in enumerate(resources):
                    resource_data['order'] = idx
                    LearningResource.objects.create(module=module, **resource_data)
                    self.stdout.write(f'  ✅ Added: {resource_data["title"]}')
                self.stdout.write(self.style.SUCCESS(f'\n✓ {len(resources)} resources added for {module.title}\n'))
            except Module.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠️  Module "{module_slug}" not found. Skipping.\n'))
        
        total = LearningResource.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully seeded {total} learning resources!'))
        self.stdout.write('\nStudents can now access curated videos, courses, books, and articles for deep dive study.\n')
