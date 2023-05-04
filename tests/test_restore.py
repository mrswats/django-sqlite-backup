from unittest.mock import patch

import pytest

from django_sqlite_backup import restore
from testing.constants import TEST_DATE_STR


def test_get_restore_class_returns_default_class():
    assert isinstance(restore.get_restore_class(), restore.SqliteRestore)


def test_get_restore_class_with_wrong_settings_raises_exception(default_settings):
    default_settings.SQLITE_BACKUP["RESTORE_CLASS"] = "foo.bar.Baz"

    with pytest.raises(ModuleNotFoundError):
        restore.get_restore_class()


def test_do_restore_calls_restore_method(default_settings):
    default_settings.SQLITE_BACKUP["RESTORE_CLASS"] = "testing.dummy_backup.DummySqliteRestore"
    with patch("testing.dummy_backup.DummySqliteRestore.restore_db") as mocked:
        restore.do_restore(TEST_DATE_STR)

    mocked.assert_called_with(TEST_DATE_STR)
