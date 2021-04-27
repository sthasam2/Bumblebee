"""
bumblebee_project URL Configuration
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("bumblebee.core.urls"), name="core"),
    path("api/auth/", include("bumblebee.users.urls"), name="users"),
]
