import os

import boto3
import pytest
from django.test import Client

from testing.constants import TEST_BUCKET_NAME
from testing.constants import TEST_DB_NAME


@pytest.fixture
def client(admin_user):
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def unauthenticated_client():
    return Client()


@pytest.fixture
def default_settings(settings):
    settings.SQLITE_BACKUP = {}
    return settings


@pytest.fixture(scope="session")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "my-id"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "my-secret"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def fake_db(tmp_path):
    dbdir = tmp_path / "db"
    dbdir.mkdir()
    db = dbdir / TEST_DB_NAME
    db.write_text("content")
    return db


@pytest.fixture
def setup_test_bucket(default_settings):
    default_settings.SQLITE_BACKUP["BUCKET_NAME"] = TEST_BUCKET_NAME
    s3 = boto3.client("s3")

    def _():
        s3.create_bucket(Bucket=TEST_BUCKET_NAME)

    return _


@pytest.fixture
def setup_sqlite_restore(setup_test_bucket, fake_db):
    def _():
        with open(fake_db) as f:
            content = f.read()

        setup_test_bucket()
        s3 = boto3.client("s3")
        s3.put_object(
            Bucket=TEST_BUCKET_NAME,
            Key=f"sqlite_backup/1992-11-25/{TEST_DB_NAME}",
            Body=content,
        )

    return _


@pytest.fixture
def test_settings(default_settings, fake_db):
    default_settings.DATABASES["default"]["NAME"] = fake_db
    return default_settings
