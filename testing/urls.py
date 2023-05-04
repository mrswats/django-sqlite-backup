from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("django_sqlite_backup.urls")),
]
