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
