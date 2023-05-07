# Django Sqlite Backup

A Django application to backup you SQLite database by calling and endpoint.

## Installation

From PYPi using `pip`:

```
pip install django-sqlite-backup
```

## Usage

Add the app to the `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    ...,
    "django_sqlite_backup",
    ...,
]
```

Then, add the app's URLs to the root URL conf:

```
    path("", include("django_sqlite_backup.urls")),
```

This will create a route in your application to backup your sqlite database:

```
GET /backup/

204: Successful backup
```

### Write your own view

If you want to use a different method or want to add some sort of authentication or other kinds of logic with the backup call, you can write your own view importing the `do_backup` function:

```
# views.py
from django.http import HttpRequest
from django.http import JsonResponse

from django_sqlite_backup import backup


def my_view(request: HttpRequest) -> JsonResponse:
    do_backup()
    return JsonResponse({}, status=204)
```

### Settings

You must define your settings in your `settings.py`:

```

SQLITE_BACKUP = {
"BACKUP_CLASS": ...,
"RESTORE_CLASS": ...,
"BUCKET_NAME": ...,
"S3_ENDPOINT": ...,
}

```

- `BACKUP_CLASS` must point to class which follows the [`SqliteBackup`](./django_sqlite_backup/backup.py) protocol.
- `RESTORE_CLASS` must point to class which follows the [`SqliteRestore`](./django_sqlite_backup/restore.py) protocol.
- `BUCKET_NAME` is the name of the bucket in S3 which can be written to.
- `S3_ENDPOINT` S3 endpoint override. Leave this blank if you use AWS S3 directly.

### Management commands

This app provides two commands for carrying out operations on the backups: `backup` and `restore`.

```console
./manage.py backup
```

Will back up the current sqlite database into the configured bucket.

```console
./manage.py restore [date_str]
```

Will restore your sqlite database from your configured bucket on the date specified.
The `date_str` is optional and defaults to today.

### AWS

By default, the backup class uses `boto3` to backup the sqlite database into S3. Therefore, you will need to also pass the [AWS Environment Variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html) to the environment where your application is running.

## Licence

This package is distributed under [MIT Licence](./LICENCE).
