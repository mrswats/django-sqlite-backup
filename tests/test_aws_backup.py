import re
from unittest.mock import patch

import boto3
import pytest
from django.conf import ImproperlyConfigured
from moto import mock_s3

from django_sqlite_backup.aws import AwsSqliteBackup
from django_sqlite_backup.backup import SqliteBackup
from tests.conftest import TEST_BUCKET_NAME
from tests.conftest import TEST_DB_NAME


@pytest.fixture
def instance():
    return AwsSqliteBackup()


@pytest.fixture
def patch_db_name(fake_db):
    with patch(
        "django_sqlite_backup.aws.AwsSqliteBackup.get_database_name",
        return_value=str(fake_db.resolve()),
    ) as db:
        yield db


def get_test_bucket():
    s3 = boto3.client("s3")
    return s3.list_objects(Bucket=TEST_BUCKET_NAME)


def test_aws_sqlite_backup_complies_with_protocol(instance):
    assert isinstance(instance, SqliteBackup)


def test_aws_sqlite_backup_returns_settings_database_name(instance, default_settings):
    assert instance.get_database_name() == default_settings.DATABASES["default"]["NAME"]


@mock_s3
@pytest.mark.usefixtures("patch_db_name", "aws_credentials")
def test_aws_sqlite_backup_raises_exception_if_bucket_name_not_defined(
    instance, setup_test_bucket, default_settings
):
    setup_test_bucket()
    del default_settings.SQLITE_BACKUP["BUCKET_NAME"]
    with pytest.raises(ImproperlyConfigured):
        instance.backup_db()


@mock_s3
@pytest.mark.usefixtures("patch_db_name", "aws_credentials")
def test_aws_sqlite_backup_sends_data_to_s3(instance, setup_test_bucket):
    setup_test_bucket()
    instance.backup_db()
    bucket = get_test_bucket()
    assert re.match(
        rf"sqlite_backup/\d{{4}}-\d{{2}}-\d{{2}}/{TEST_DB_NAME}", bucket["Contents"][0]["Key"]
    )
