from django.core.management.base import BaseCommand

from django_sqlite_backup import list_backups


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        backups = list_backups.do_list()

        for backup in backups:
            self.stdout.write(backup)
