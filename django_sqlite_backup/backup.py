import importlib
from typing import Protocol
from typing import runtime_checkable
from typing import Type

from django.conf import settings


@runtime_checkable
class SqliteBackup(Protocol):
    def backup_db(self) -> None:
        ...

    def get_database_name(self) -> str:
        ...


DEFAULT_BACKUP_CLASS = "django_sqlite_backup.aws.AwsSqliteBackup"

SQLITE_BACKUP = {
    "BACKUP_CLASS": DEFAULT_BACKUP_CLASS,
    "BUCKET_NAME": "",
}


def get_backup_class() -> Type[SqliteBackup]:
    class_string = (
        getattr(settings, "SQLITE_BACKUP", {}).get("BACKUP_CLASS") or DEFAULT_BACKUP_CLASS
    )
    split_stirng = class_string.split(".")
    module_name, class_name = split_stirng[:-1], split_stirng[-1]
    module = importlib.import_module(".".join(module_name))
    return getattr(module, class_name)
