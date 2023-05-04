from typing import Protocol
from typing import runtime_checkable
from typing import Type

from django.conf import settings
from django.utils.module_loading import import_string


@runtime_checkable
class SqliteRestore(Protocol):
    def restore_db(self, date_str: str) -> None:
        ...


DEFAULT_RESTORE_CLASS = "django_sqlite_backup.aws.AwsRestoreDb"


def get_restore_class() -> Type[SqliteRestore]:
    class_string = (
        getattr(settings, "SQLITE_BACKUP", {}).get("RESTORE_CLASS") or DEFAULT_RESTORE_CLASS
    )

    return import_string(class_string)


def do_restore(date_str: str) -> None:
    restore_class = get_restore_class()
    restore_class_instance = restore_class()
    restore_class_instance.restore_db(date_str)
