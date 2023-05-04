from unittest.mock import patch

import pytest
from django.core.management import call_command

from testing.constants import TEST_DATE_STR


@pytest.fixture
def mock_restore():
    with patch("django_sqlite_backup.restore.do_restore") as mocked:
        yield mocked


@pytest.fixture
def restore_run(mock_restore):
    def _(*args, **kwatgs):
        call_command("restore", TEST_DATE_STR)

    return _


def test_backup_command_writes_to_stdout_on_success(restore_run, capsys):
    restore_run()
    out, err = capsys.readouterr()
    assert out == "Restore complete!\n"
    assert err == ""


def test_backup_command_calls_do_restore(restore_run, mock_restore):
    restore_run()
    mock_restore.assert_called_with("1992-11-25")
