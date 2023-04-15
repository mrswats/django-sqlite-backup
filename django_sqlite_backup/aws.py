from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Union

import boto3
from django.conf import ImproperlyConfigured
from django.conf import settings


class AwsSqliteBackup:
    def __init__(self) -> None:
        self.s3 = boto3.resource("s3")
        self._db_name: Union[str, None] = None

    def get_database_name(self) -> Union[str, Path]:
        if self._db_name is None:
            self._db_name = settings.DATABASES["default"]["name"]

        return self._db_name

    def _read_db(self) -> Any:
        with open(self.get_database_name()) as f:
            return f

    def backup_db(self) -> None:
        bucket_name = settings.SQLITE_BACKUP.get("BUCKET_NAME")
        db_name = self.get_database_name()

        if bucket_name is None:
            raise ImproperlyConfigured("`BUCKET_NAME` is not defined")

        full_bucket_name = f"{bucket_name}/{datetime.now().strftime('%Y-%m-%d')}/{db_name}"

        self.s3.put_object(full_bucket_name)
