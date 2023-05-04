import re

import pytest
from django.conf import ImproperlyConfigured
from moto import mock_s3

from django_sqlite_backup.aws import AwsSqliteBackup
from django_sqlite_backup.aws import get_database_name
from django_sqlite_backup.backup import SqliteBackup
from testing import helpers
from testing.constants import TEST_DB_NAME


@pytest.fixture(scope="session")
def instance(aws_credentials):
    return AwsSqliteBackup()


def test_aws_sqlite_backup_complies_with_protocol(instance):
    assert isinstance(instance, SqliteBackup)


def test_aws_sqlite_backup_returns_settings_database_name(default_settings):
    assert get_database_name() == default_settings.DATABASES["default"]["NAME"]


@mock_s3
@pytest.mark.usefixtures("test_settings", "aws_credentials")
def test_aws_sqlite_backup_raises_exception_if_bucket_name_not_defined(
    instance, setup_test_bucket, default_settings
):
    setup_test_bucket()
    del default_settings.SQLITE_BACKUP["BUCKET_NAME"]
    with pytest.raises(ImproperlyConfigured):
        instance.backup_db()


@mock_s3
@pytest.mark.usefixtures("test_settings", "aws_credentials")
def test_aws_sqlite_backup_sends_data_to_s3(instance, setup_test_bucket):
    setup_test_bucket()
    instance.backup_db()
    bucket = helpers.get_test_bucket()
    assert re.match(
        rf"sqlite_backup/\d{{4}}-\d{{2}}-\d{{2}}/{TEST_DB_NAME}", bucket["Contents"][0]["Key"]
    )
