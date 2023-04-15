import pytest
from django.urls import reverse


@pytest.fixture
def dummy_backup_settings(default_settings):
    default_settings.SQLITE_BACKUP["BACKUP_CLASS"] = "testing.dummy_backup.DummySqliteBackup"


@pytest.fixture
def backup_url():
    return reverse("sqlite-backup")


@pytest.fixture
def backup_view_response(client, backup_url):
    return client.post(backup_url)


def test_sqlite_backup_url(backup_url):
    assert backup_url == "/backup/"


def test_backup_view_requires_login(unauthenticated_client, backup_url):
    response = unauthenticated_client.post(backup_url)
    assert response.status_code == 403


def test_backup_view_accepts_only_post(client, backup_url):
    response = client.get(backup_url)
    assert response.status_code == 405


@pytest.mark.django_db
@pytest.mark.usefixtures("dummy_backup_settings")
def test_backup_view_returns_empty_response(backup_view_response):
    assert backup_view_response.content.decode() == ""


@pytest.mark.django_db
@pytest.mark.usefixtures("dummy_backup_settings")
def test_backup_view_returns_empty_response_code(backup_view_response):
    assert backup_view_response.status_code == 204
