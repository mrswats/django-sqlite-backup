from unittest.mock import patch

import pytest

from django_sqlite_backup import list_backups
from django_sqlite_backup.aws import AwsListDb


def test_get_list_class_returns_default_value():
    cls = list_backups.get_list_class()
    assert cls is AwsListDb


def test_get_backup_class_with_wrong_settings_raises_exception(default_settings):
    default_settings.SQLITE_BACKUP["LIST_CLASS"] = "foo.bar.Baz"

    with pytest.raises(ModuleNotFoundError):
        list_backups.get_list_class()


def test_do_list_backups_calls_do_list_method(default_settings):
    default_settings.SQLITE_BACKUP["LIST_CLASS"] = "testing.dummy_backup.DummyListBackups"

    with patch("testing.dummy_backup.DummyListBackups.list_db") as mocked:
        list_backups.do_list()

    mocked.assert_called_with()
