from datetime import datetime
from typing import Any

import boto3
from django.conf import ImproperlyConfigured
from django.conf import settings


class AwsSqliteBackup:
    def __init__(self) -> None:
        self.s3 = boto3.client("s3")

    def get_database_name(self) -> str:
        return str(settings.DATABASES["default"]["NAME"])

    def _read_db(self) -> Any:
        with open(self.get_database_name()) as f:
            return f.read()

    def backup_db(self) -> None:
        bucket_name = settings.SQLITE_BACKUP.get("BUCKET_NAME")
        db_name = self.get_database_name().split("/")[-1]

        if bucket_name is None:
            raise ImproperlyConfigured("`BUCKET_NAME` is not defined")

        full_bucket_name = f"sqlite_backup/{datetime.now().strftime('%Y-%m-%d')}/{db_name}"

        self.s3.put_object(
            Bucket=bucket_name,
            Key=full_bucket_name,
            Body=self._read_db(),
        )


class AwsRestoreDb:
    def __init__(self) -> None:
        self.s3 = boto3.client("s3")

    def get_database_name(self) -> str:
        return str(settings.DATABASES["default"]["NAME"])

    def restore_db(self, date_str: str) -> None:
        bucket_name = settings.SQLITE_BACKUP.get("BUCKET_NAME")

        if bucket_name is None:
            raise ImproperlyConfigured("`BUCKET_NAME` is not defined")

        db_name = self.get_database_name()
        key = f"sqlite_backup/{date_str}/{db_name}"

        response = self.s3.get_object(
            Bucket=bucket_name,
            Key=key,
        )

        with open(db_name, "w") as f:
            f.write(response.get("Body").read().decode())
