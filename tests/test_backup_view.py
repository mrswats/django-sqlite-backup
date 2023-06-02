import pytest
from django.test import RequestFactory
from django.urls import reverse

from django_sqlite_backup.views import backup_view


@pytest.fixture
def dummy_backup_settings(default_settings):
    default_settings.SQLITE_BACKUP["BACKUP_CLASS"] = "testing.dummy_backup.DummySqliteBackup"
    default_settings.SQLITE_BACKUP["BUCKET_NAME"] = "bucket-name"


@pytest.fixture
def backup_url():
    return reverse("sqlite-backup")


@pytest.fixture
def backup_view_response(backup_url):
    request = RequestFactory().get(backup_url)
    return backup_view(request)


def test_sqlite_backup_url(backup_url):
    assert backup_url == "/backup/"


@pytest.mark.django_db
@pytest.mark.usefixtures("dummy_backup_settings")
def test_backup_view_response_attrs(mock_backup, backup_view_response):
    assert backup_view_response.status_code == 204
    assert backup_view_response.content.decode() == "{}"
    mock_backup.assert_called_once()


@pytest.mark.django_db
@pytest.mark.usefixtures("dummy_backup_settings")
def test_backup_view_response(client, backup_url):
    response = client.get(backup_url)
    assert response.status_code == 204
    assert response.content.decode() == ""
