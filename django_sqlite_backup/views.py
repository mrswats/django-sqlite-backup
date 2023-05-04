from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from django_sqlite_backup import backup
from django_sqlite_backup.decorators import login_required


@login_required
@require_http_methods(["POST"])
def backup_view(request: HttpRequest) -> JsonResponse:
    backup.do_backup()
    return JsonResponse({}, status=204)
