from django.http import HttpRequest
from django.http import JsonResponse

from django_sqlite_backup import backup


def backup_view(request: HttpRequest) -> JsonResponse:
    backup.do_backup()
    return JsonResponse({}, status=204)
