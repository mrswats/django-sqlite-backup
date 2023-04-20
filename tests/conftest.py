import os

import pytest
from django.test import Client


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


@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "my-id"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "my-secret"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
