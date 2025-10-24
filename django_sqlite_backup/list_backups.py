from typing import Protocol
from typing import runtime_checkable

from django.conf import settings
from django.utils.module_loading import import_string


@runtime_checkable
class SqliteList(Protocol):
    def list_db(self) -> list[str]:
        pass


DEFAULT_LIST_CLASS = "django_sqlite_backup.aws.AwsListDb"


def get_list_class() -> type[SqliteList]:
    class_string = getattr(settings, "SQLITE_BACKUP", {}).get("LIST_CLASS") or DEFAULT_LIST_CLASS

    return import_string(class_string)


def do_list() -> list[str]:
    list_class = get_list_class()
    list_class_instance = list_class()
    return list_class_instance.list_db()
