from functools import wraps
from typing import Any
from typing import Callable

from django.http import HttpRequest
from django.http import HttpResponse


def login_required(view_function) -> Callable[[HttpRequest, Any], HttpResponse]:
    @wraps(view_function)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return view_function(request, *args, **kwargs)

        return HttpResponse(status=403)

    return wrapper
