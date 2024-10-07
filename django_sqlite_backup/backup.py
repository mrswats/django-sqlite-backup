from typing import Protocol
from typing import runtime_checkable
from typing import Type

from django.conf import settings
from django.utils.module_loading import import_string


@runtime_checkable
class SqliteBackup(Protocol):
    def backup_db(self) -> None: ...


DEFAULT_BACKUP_CLASS = "django_sqlite_backup.aws.AwsSqliteBackup"

SQLITE_BACKUP = {
    "BACKUP_CLASS": DEFAULT_BACKUP_CLASS,
    "BUCKET_NAME": "",
}


def get_backup_class() -> Type[SqliteBackup]:
    class_string = (
        getattr(settings, "SQLITE_BACKUP", {}).get("BACKUP_CLASS") or DEFAULT_BACKUP_CLASS
    )

    return import_string(class_string)


def do_backup() -> None:
    backup_class = get_backup_class()
    backup_class_instance = backup_class()
    backup_class_instance.backup_db()
