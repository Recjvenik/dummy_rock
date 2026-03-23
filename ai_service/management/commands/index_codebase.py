"""
Management command: index_codebase
Indexes the AI Lab Django project using jCodeMunch for token-efficient code search.

Usage:
    python manage.py index_codebase
    python manage.py index_codebase --force
"""
from django.core.management.base import BaseCommand
from ai_service import codemunch


class Command(BaseCommand):
    help = 'Index the AI Lab codebase with jCodeMunch for token-efficient AI code exploration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-index even if already indexed',
        )

    def handle(self, *args, **options):
        force = options['force']

        if codemunch.is_indexed() and not force:
            self.stdout.write(self.style.WARNING(
                'Codebase already indexed. Use --force to re-index.'
            ))
            return

        self.stdout.write('Indexing AI Lab codebase with jCodeMunch...')
        self.stdout.write(f'  Storage: {codemunch.INDEX_PATH}')

        try:
            result = codemunch.index_project(force=force)

            if 'error' in result:
                self.stderr.write(self.style.ERROR(f'Indexing failed: {result["error"]}'))
                return

            # Print summary stats
            stats = result.get('stats', result)
            self.stdout.write(self.style.SUCCESS('Codebase indexed successfully!'))

            if isinstance(stats, dict):
                for key, val in stats.items():
                    if key != 'error':
                        self.stdout.write(f'  {key}: {val}')

            self.stdout.write('')
            self.stdout.write('Students can now use the Code Explorer in AI Chat to explore')
            self.stdout.write('the AI Lab source code with 80-99% token savings.')

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
            raise
