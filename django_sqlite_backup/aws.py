from datetime import datetime
from functools import lru_cache
from typing import Any

import boto3
from django.conf import ImproperlyConfigured
from django.conf import settings


@lru_cache
def s3():
    return boto3.client(
        "s3",
        endpoint_url=settings.SQLITE_BACKUP.get("S3_ENDPOINT"),
    )


def get_database_name() -> str:
    return str(settings.DATABASES["default"]["NAME"])


class AwsSqliteBackup:
    def _read_db(self) -> Any:
        with open(get_database_name(), "rb") as f:
            return f.read()

    def backup_db(self) -> None:
        bucket_name = settings.SQLITE_BACKUP.get("BUCKET_NAME")
        db_name = get_database_name().split("/")[-1]

        if bucket_name is None:
            raise ImproperlyConfigured("`BUCKET_NAME` is not defined")

        full_bucket_name = f"sqlite_backup/{datetime.now().strftime('%Y-%m-%d')}/{db_name}"

        s3().put_object(
            Bucket=bucket_name,
            Key=full_bucket_name,
            Body=self._read_db(),
        )


class AwsRestoreDb:
    def restore_db(self, date_str: str) -> None:
        bucket_name = settings.SQLITE_BACKUP.get("BUCKET_NAME")

        if bucket_name is None:
            raise ImproperlyConfigured("`BUCKET_NAME` is not defined")

        db_name = get_database_name()
        key = f"sqlite_backup/{date_str}/{db_name}"

        response = s3().get_object(
            Bucket=bucket_name,
            Key=key,
        )

        with open(db_name, "wb") as f:
            f.write(response.get("Body").read())


class AwsListDb:
    def list_db(self) -> list[str]:
        bucket_name = settings.SQLITE_BACKUP.get("BUCKET_NAME")

        if bucket_name is None:
            raise ImproperlyConfigured("`BUCKET_NAME` is not defined")

        response = s3().list_objects(
            Bucket=bucket_name,
        )

        return [backup_date["Key"] for backup_date in response["Contents"]]
