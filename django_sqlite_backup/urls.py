from django.url import path

from django_sqlite_backup import views

urlpatterns = [
    path("backup", views.backup),
]
