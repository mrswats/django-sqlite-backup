import pytest

from django_sqlite_backup import backup
from django_sqlite_backup.aws import AwsSqliteBackup


def test_get_backup_class_returns_default_value():
    cls = backup.get_backup_class()
    assert cls is AwsSqliteBackup


def test_get_backup_class_with_wrong_settings_raises_exception(default_settings):
    default_settings.SQLITE_BACKUP["BACKUP_CLASS"] = "foo.bar.Baz"

    with pytest.raises(ModuleNotFoundError):
        backup.get_backup_class()
