from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser

from django_sqlite_backup import restore


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "restore_date",
            help="Date to restore from. Format yy-mm-dd.",
            default=datetime.now().strftime("%Y-%m-%d"),
            type=str,
        )

    def handle(self, *args, **options) -> None:
        restore.do_restore(options["restore_date"])
        self.stdout.write("Restore complete!")
