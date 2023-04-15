from django.urls import path

from django_sqlite_backup import views

urlpatterns = [
    path("backup/", views.backup_view, name="sqlite-backup"),
]
