"""
comment-crud
comment-list
comment-detail
"""

from django.urls import path

from bumblebee.connections.api.views.connection_views import (
    AcceptFollowRequestView,
    BlockUnblockView,
    DeleteFollowerView,
    DeleteFollowRequestView,
    FollowUnfollowRequestUnrequestView,
    MuteUnmuteView,
    RetrieveBlockedIDListView,
    RetrieveConnectionListView,
    RetrieveFollowerListView,
    RetrieveFollowingListView,
    RetrieveMutedIDListView,
    RetrieveUserConnectionListView,
)

urlpatterns = [
    # retrieve
    path(
        "list",
        RetrieveConnectionListView.as_view(),
        name="connection-list",
    ),
    path(
        "user/username=<str:username>/connection/list",
        RetrieveUserConnectionListView.as_view(),
        name="user-connection-list",
    ),
    path(
        "user/username=<str:username>/follower/detail",
        RetrieveFollowerListView.as_view(),
        name="follower-detail",
    ),
    path(
        "user/username=<str:username>/following/detail",
        RetrieveFollowingListView.as_view(),
        name="following-detailt",
    ),
    path(
        "user/muted/detail",
        RetrieveMutedIDListView.as_view(),
        name="create-muted-detail",
    ),
    path(
        "user/blocked/detail",
        RetrieveBlockedIDListView.as_view(),
        name="blocked-detail",
    ),
    # create
    path(
        "user/follow/accept",
        AcceptFollowRequestView.as_view(),
        name="accept-follow",
    ),
    path(
        "user/follow",
        FollowUnfollowRequestUnrequestView.as_view(),
        name="follow-user",
    ),
    path(
        "user/block",
        BlockUnblockView.as_view(),
        name="block-user",
    ),
    path(
        "user/mute",
        MuteUnmuteView.as_view(),
        name="mute-user",
    ),
    # delete
    path(
        "user/follower_request/delete",
        DeleteFollowRequestView.as_view(),
        name="delete-follower-request",
    ),
    path(
        "user/follower/delete",
        DeleteFollowerView.as_view(),
        name="delete-follower",
    ),
]
