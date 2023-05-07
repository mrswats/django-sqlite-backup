import pytest
from django.urls import reverse


@pytest.fixture
def dummy_backup_settings(default_settings):
    default_settings.SQLITE_BACKUP["BACKUP_CLASS"] = "testing.dummy_backup.DummySqliteBackup"
    default_settings.SQLITE_BACKUP["BUCKET_NAME"] = "bucket-name"


@pytest.fixture
def backup_url():
    return reverse("sqlite-backup")


@pytest.fixture
def backup_view_response(client, backup_url):
    return client.get(backup_url)


def test_sqlite_backup_url(backup_url):
    assert backup_url == "/backup/"


@pytest.mark.django_db
@pytest.mark.usefixtures("dummy_backup_settings")
def test_backup_view_returns_empty_response(backup_view_response):
    assert backup_view_response.content.decode() == ""


@pytest.mark.django_db
@pytest.mark.usefixtures("dummy_backup_settings")
def test_backup_view_returns_empty_response_code(backup_view_response):
    assert backup_view_response.status_code == 204
