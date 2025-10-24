from unittest.mock import patch

import pytest
from django.core.management import call_command


@pytest.fixture
def mock_backup():
    with patch(
        "django_sqlite_backup.list_backups.do_list",
        return_value=["foo/bar/baz.db"],
    ) as mocked:
        yield mocked


@pytest.fixture
def list_run(mock_backup):
    def _(*args, **kwatgs):
        call_command("list_backups")

    return _


def test_list_backups_command_writes_to_stdout_on_success(list_run, capsys):
    list_run()
    out, err = capsys.readouterr()
    assert out == "foo/bar/baz.db\n"
    assert err == ""
