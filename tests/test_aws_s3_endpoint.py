import pytest

from django_sqlite_backup.aws import s3


@pytest.fixture
def client():
    def _():
        s3.cache_clear()
        return s3()

    return _


def test_s3_endpoint_url(default_settings, client):
    endpoint_url = "http://example.com"
    default_settings.SQLITE_BACKUP["S3_ENDPOINT"] = endpoint_url
    assert client().meta.endpoint_url == endpoint_url


@pytest.mark.usefixtures("default_settings")
def test_s3_default_endpoint_url(client):
    assert client().meta.endpoint_url == "https://s3.amazonaws.com"
