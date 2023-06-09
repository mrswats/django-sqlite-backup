from unittest.mock import patch

import pytest
from django.core.management import call_command


@pytest.fixture
def mock_backup():
    with patch("django_sqlite_backup.backup.do_backup") as mocked:
        yield mocked


@pytest.fixture
def backup_run(mock_backup):
    def _(*args, **kwatgs):
        call_command("backup")

    return _


def test_backup_command_writes_to_stdout_on_success(backup_run, capsys):
    backup_run()
    out, err = capsys.readouterr()
    assert out == "Backup done!\n"
    assert err == ""
