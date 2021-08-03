"""
bumblebee_project URL Configuration
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.definitions import DEBUG
from config.settings.local import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("bumblebee.core.urls"), name="core"),
    path("api/auth/", include("bumblebee.users.urls"), name="users"),
    path("api/profile/", include("bumblebee.profiles.urls"), name="profiles"),
    path("api/content/", include("bumblebee.buzzes.urls"), name="buzzes"),
    path("api/comment/", include("bumblebee.comments.urls"), name="comments"),
    path("api/connection/", include("bumblebee.connections.urls"), name="connections"),
    path("api/feed/", include("bumblebee.feeds.urls"), name="feeds"),
    path(
        "api/notification/",
        include("bumblebee.notifications.urls"),
        name="notifications",
    ),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
