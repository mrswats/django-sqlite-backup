import pytest
from django.conf import ImproperlyConfigured
from moto import mock_aws

from django_sqlite_backup.aws import AwsListDb
from testing.constants import TEST_DATE_STR
from testing.constants import TEST_DB_NAME


@pytest.fixture
def instance():
    return AwsListDb()


@mock_aws
@pytest.mark.usefixtures("aws_credentials")
def test_aws_sqlite_list_db_raises_exception_if_bucket_name_not_defined(
    instance, setup_test_bucket, test_settings
):
    setup_test_bucket()
    del test_settings.SQLITE_BACKUP["BUCKET_NAME"]
    with pytest.raises(ImproperlyConfigured):
        instance.list_db()


@mock_aws
@pytest.mark.usefixtures("aws_credentials")
def test_aws_sqlite_list_db_returns_list_of_backups(
    instance, setup_sqlite_restore, default_settings, fake_db
):
    setup_sqlite_restore()
    default_settings.DATABASES["default"]["NAME"] = TEST_DB_NAME
    assert instance.list_db() == [f"sqlite_backup/{TEST_DATE_STR}/fake.db"]
