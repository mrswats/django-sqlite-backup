import pytest

from django_sqlite_backup.aws import AwsSqliteBackup
from django_sqlite_backup.backup import SqliteBackup


@pytest.fixture
def instance():
    return AwsSqliteBackup()


def test_aws_sqlite_backup_complies_with_protocol(instance):
    assert isinstance(instance, SqliteBackup)
