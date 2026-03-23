"""
Management command: generate_daily_challenge

Usage:
    python manage.py generate_daily_challenge
    python manage.py generate_daily_challenge --date 2025-06-01
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from school.models import DailyChallenge
from modules.models import Module
import random


CHALLENGE_TEMPLATES = [
    ('quiz', 'AI Terms Quiz', 'Look up 3 glossary terms from today\'s module and write a sentence using each.'),
    ('lab', 'Lab Sprint', 'Complete one interactive lab session and screenshot your result.'),
    ('glossary', 'Define & Apply', 'Find the definition of a key AI term and explain it to a friend in your own words.'),
    ('streak', 'Daily Streak', 'Log in, complete any activity, and maintain your learning streak!'),
]


class Command(BaseCommand):
    help = 'Generate a daily challenge for today (or a specified date).'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='Date in YYYY-MM-DD format (default: today)')
        parser.add_argument('--xp', type=int, default=25, help='XP reward for the challenge')

    def handle(self, *args, **options):
        if options['date']:
            from datetime import date
            target_date = date.fromisoformat(options['date'])
        else:
            target_date = timezone.now().date()

        if DailyChallenge.objects.filter(date=target_date).exists():
            self.stdout.write(self.style.WARNING(f'Challenge for {target_date} already exists. Skipping.'))
            return

        challenge_type, title, description = random.choice(CHALLENGE_TEMPLATES)
        module = Module.objects.filter(is_published=True).order_by('?').first()

        challenge = DailyChallenge.objects.create(
            date=target_date,
            title=title,
            description=description,
            challenge_type=challenge_type,
            target_module=module,
            xp_reward=options['xp'],
        )
        self.stdout.write(self.style.SUCCESS(
            f'Created challenge for {target_date}: "{challenge.title}" (+{challenge.xp_reward} XP)'
        ))
