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

`/backup/` which accepts only `POST` requests with authentication.

If the request succeeds it will return a `294`. Otherwise, a `403` if the request was not authenticated.

### Settings

You must define your settings in your `settings.py`:

```
SQLITE_BACKUP = {
    "BACKUP_CLASS": ...,
    "RESTORE_CLASS": ...,
    "BUCKET_NAME": ...,
}
```

- `BACKUP_CLASS` must point to class which follows the [`SqliteBackup`](./django_sqlite_backup/backup.py) protocol.
- `RESTORE_CLASS` must point to class which follows the [`SqliteRestore`](./django_sqlite_backup/restore.py) protocol.
- `BUCKET_NAME` is the name of the bucket in S3 which can be written to.

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
