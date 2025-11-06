'''
Command to create a backup of the database file.
'''
import datetime
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = __doc__.strip()

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-dumps', dest='max_dumps', type=int, default=5,
            help='Maximum number of database dump files to keep.'
        )

    def handle(self, *args, **options):
        self.stdout.write('---- Dumping database ----')
        dumps_dir = settings.PRIVATE_DIR / 'dbdumps'

        # Copy the database file
        dump_path = None
        db_path = None
        if hasattr(settings, 'DATABASES') and settings.DATABASES.get('default'):
            dbs = settings.DATABASES.get('default')
            now = datetime.datetime.now()
            if 'sqlite' in dbs.get('ENGINE') and dbs.get('NAME'):
                db_path = Path(dbs['NAME'])
                if db_path.exists():
                    dump_path = dumps_dir / f'{now.strftime("%Y-%m-%d_%H-%M-%S")}.sqlite3'
            else:
                raise CommandError('Error: The database engine is not handled.')
        if not db_path or not dump_path:
            self.stdout.write('No database file configured, dump command ignored.')
            return
        dumps_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(db_path, dump_path)
        self.stdout.write(f'Database dumped to {dump_path}.')

        # Remove old dumps
        self.stdout.write('Searching for old database dump to remove...')
        dumps = [
            (path.stat().st_mtime, path)
            for path in dumps_dir.iterdir()
            if path.name.endswith('.sqlite3')
        ]
        removed = 0
        if dumps:
            dumps.sort()
            while len(dumps) >= options['max_dumps']:
                path = dumps.pop(0)[1]
                self.stdout.write(f'Removing old database dump "{path}".')
                path.unlink()
                removed += 1
        if not removed:
            self.stdout.write('No old database dump file to remove.')
