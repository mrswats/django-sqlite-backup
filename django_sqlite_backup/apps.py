from django.apps import AppConfig
from django.conf import ImproperlyConfigured
from django.conf import settings


class DjangoSqliteBackupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_sqlite_backup"

    def ready(self) -> None:
        if settings.DATABASES["default"]["ENGINE"] != "django.db.backends.sqlite3":
            raise ImproperlyConfigured("'default' database must be a SQLite database.")
