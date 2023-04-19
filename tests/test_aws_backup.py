import pytest
from moto import mock_s3

from django_sqlite_backup.aws import AwsSqliteBackup
from django_sqlite_backup.backup import SqliteBackup


@pytest.fixture
def instance():
    return AwsSqliteBackup()


def test_aws_sqlite_backup_complies_with_protocol(instance):
    assert isinstance(instance, SqliteBackup)


@mock_s3
def test_aws_sqlite_backup_sends_data_to_s3(instance, default_settings):
    default_settings.SQLITE_BACKUP["BUCKET_NAME"] = "mock-bucket"
    # TODO: Create a temp file to "upload" to s3
    instance.backup_db()
