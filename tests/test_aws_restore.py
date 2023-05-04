from unittest.mock import patch

import pytest
import time_machine
from django.conf import ImproperlyConfigured
from moto import mock_s3

from django_sqlite_backup.aws import AwsRestoreDb
from tests.conftest import TEST_DATE
from tests.conftest import TEST_DATE_STR
from tests.conftest import TEST_DB_NAME


@pytest.fixture
def set_time():
    with time_machine.travel(TEST_DATE, tick=False):
        yield TEST_DATE


@pytest.fixture
def instance():
    return AwsRestoreDb()


@pytest.fixture
def patch_db_name(fake_db):
    with patch(
        "django_sqlite_backup.aws.AwsRestoreDb.get_database_name",
        return_value=fake_db,
    ) as db:
        yield db


def test_aws_sqlite_retroe_returns_settings_database_name(instance, default_settings):
    assert instance.get_database_name() == default_settings.DATABASES["default"]["NAME"]


@mock_s3
@pytest.mark.usefixtures("patch_db_name", "aws_credentials")
def test_aws_sqlite_backup_raises_exception_if_bucket_name_not_defined(
    instance, setup_test_bucket, default_settings
):
    setup_test_bucket()
    del default_settings.SQLITE_BACKUP["BUCKET_NAME"]
    with pytest.raises(ImproperlyConfigured):
        instance.restore_db(TEST_DATE_STR)


@mock_s3
@pytest.mark.usefixtures("aws_credentials", "set_time")
def test_aws_sqlite_restore_donwloads_the_sqlite_dhtabase(
    instance, setup_sqlite_restore, default_settings, fake_db
):
    setup_sqlite_restore()
    default_settings.DATABASES["default"]["NAME"] = TEST_DB_NAME
    instance.restore_db(TEST_DATE_STR)

    with open(fake_db) as f:
        assert f.read() == "content"
