import pytest
from django.apps.registry import Apps
from django.conf import ImproperlyConfigured

DJANGO_SQLITE_BACKUP = "django_sqlite_backup"


def test_app_not_ready_raises_error_if_sqlite_database_is_not_default_db(default_settings):
    apps = Apps(installed_apps=[DJANGO_SQLITE_BACKUP])
    dsb_config = apps.get_app_config(DJANGO_SQLITE_BACKUP)

    default_settings.DATABASES["default"]["ENGINE"] = "something-else"

    with pytest.raises(ImproperlyConfigured):
        dsb_config.ready()
