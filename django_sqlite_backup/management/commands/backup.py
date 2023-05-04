from django.core.management.base import BaseCommand

from django_sqlite_backup import backup


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        backup.do_backup()
        self.stdout.write("Backup done!")
