from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from django_sqlite_backup import backup
from django_sqlite_backup.decorators import login_required


@login_required
@require_http_methods(["POST"])
def backup_view(request: HttpRequest) -> JsonResponse:
    backup_class = backup.get_backup_class()
    backup_class_instance = backup_class()
    backup_class_instance.backup_db()

    return JsonResponse({}, status=204)
