from django.core.management.base import BaseCommand
from gamification.models import Badge

BADGES = [
    {'slug': 'first_step',      'name': 'First Step',      'icon': '🚀', 'color': '#00ff88', 'category': 'learn',   'xp_reward': 0,   'description': 'Complete your first section'},
    {'slug': 'quiz_master',     'name': 'Quiz Master',     'icon': '🎯', 'color': '#ffd700', 'category': 'learn',   'xp_reward': 50,  'description': 'Score 100% on any quiz'},
    {'slug': 'neural_architect','name': 'Neural Architect','icon': '🧠', 'color': '#4fc3f7', 'category': 'learn',   'xp_reward': 100, 'description': 'Complete the Neural Network module'},
    {'slug': 'rag_builder',     'name': 'RAG Builder',     'icon': '🔍', 'color': '#ce93d8', 'category': 'explore', 'xp_reward': 100, 'description': 'Complete the LLM Systems module'},
    {'slug': 'agent_designer',  'name': 'Agent Designer',  'icon': '🤖', 'color': '#ffb74d', 'category': 'explore', 'xp_reward': 100, 'description': 'Complete the Agentic AI module'},
    {'slug': 'code_explorer',   'name': 'Code Explorer',   'icon': '💻', 'color': '#00bcd4', 'category': 'explore', 'xp_reward': 50,  'description': 'Use the Code Explorer 10 times'},
    {'slug': 'streak_7',        'name': 'Week Warrior',    'icon': '🔥', 'color': '#ef5350', 'category': 'streak',  'xp_reward': 100, 'description': '7-day learning streak'},
    {'slug': 'streak_30',       'name': 'Month Master',    'icon': '⚡', 'color': '#ffd700', 'category': 'streak',  'xp_reward': 500, 'description': '30-day learning streak'},
    {'slug': 'sim_runner',      'name': 'Simulator',       'icon': '⚙️', 'color': '#26a69a', 'category': 'explore', 'xp_reward': 25,  'description': 'Run 10 simulations'},
    {'slug': 'ai_whisperer',    'name': 'AI Whisperer',    'icon': '💬', 'color': '#f48fb1', 'category': 'social',  'xp_reward': 50,  'description': 'Chat with AI 20 times'},
    {'slug': 'speed_learner',   'name': 'Speed Learner',   'icon': '⏩', 'color': '#aed581', 'category': 'learn',   'xp_reward': 75,  'description': 'Complete a module in under 30 minutes'},
    {'slug': 'completionist',   'name': 'Completionist',   'icon': '🏆', 'color': '#ffd700', 'category': 'learn',   'xp_reward': 500, 'description': 'Complete all 7 AI modules'},
]


class Command(BaseCommand):
    help = 'Seed badge definitions'

    def handle(self, *args, **options):
        created = 0
        for b in BADGES:
            _, was_created = Badge.objects.get_or_create(slug=b['slug'], defaults=b)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} new badges ({len(BADGES)} total)'))
