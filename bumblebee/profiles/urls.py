from django.urls import path

from bumblebee.profiles.api.views import (
    ProfileDetailView,
    ProfileImageUploadView,
    ProfileSummaryView,
    UpdateProfileView,
    ChangePrivateProfileView,
)

from .models import Profile

urlpatterns = [
    path(
        "detail/user=<slug:username>",
        ProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path(
        "summary/user=<slug:username>",
        ProfileSummaryView.as_view(),
        name="profile-summary",
    ),
    path(
        "update/user=<slug:username>",
        UpdateProfileView.as_view(),
        name="update-profile",
    ),
    path(
        "change_private/user=<slug:username>",
        ChangePrivateProfileView.as_view(),
        name="update-profile",
    ),
    path(
        "upload_images/user=<slug:username>",
        ProfileImageUploadView.as_view(),
        name="update-profile",
    ),
]
