import pytest
import time_machine
from django.conf import ImproperlyConfigured
from moto import mock_aws

from django_sqlite_backup.aws import AwsRestoreDb
from django_sqlite_backup.aws import get_database_name
from testing.constants import TEST_DATE
from testing.constants import TEST_DATE_STR
from testing.constants import TEST_DB_NAME


@pytest.fixture
def set_time():
    with time_machine.travel(TEST_DATE, tick=False):
        yield TEST_DATE


@pytest.fixture
def instance():
    return AwsRestoreDb()


def test_aws_sqlite_restore_returns_settings_database_name(default_settings):
    assert get_database_name() == str(default_settings.DATABASES["default"]["NAME"])


@mock_aws
@pytest.mark.usefixtures("aws_credentials")
def test_aws_sqlite_backup_raises_exception_if_bucket_name_not_defined(
    instance, setup_test_bucket, test_settings
):
    setup_test_bucket()
    del test_settings.SQLITE_BACKUP["BUCKET_NAME"]
    with pytest.raises(ImproperlyConfigured):
        instance.restore_db(TEST_DATE_STR)


@mock_aws
@pytest.mark.usefixtures("aws_credentials", "set_time")
def test_aws_sqlite_restore_donwloads_the_sqlite_dhtabase(
    instance, setup_sqlite_restore, default_settings, fake_db
):
    setup_sqlite_restore()
    default_settings.DATABASES["default"]["NAME"] = TEST_DB_NAME
    instance.restore_db(TEST_DATE_STR)

    with open(fake_db, "rb") as f:
        assert f.read() == b"content"
