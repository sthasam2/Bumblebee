from django.urls import path

from bumblebee.buzzes.api.views.buzz_views import (
    BuzzDetailView,
    BuzzListView,
    UserBuzzListView,
    CreateBuzzView,
    EditBuzzView,
    DeleteBuzzView,
)

from bumblebee.buzzes.api.views.rebuzz_views import (
    RebuzzDetailView,
    RebuzzListView,
    UserRebuzzListView,
    CreateRebuzzView,
    EditRebuzzView,
    DeleteRebuzzView,
)

from bumblebee.buzzes.api.views.interactions_views import (
    UpvoteBuzzView,
    DownvoteBuzzView,
    UpvoteRebuzzView,
    DownvoteRebuzzView,
)


buzz = [
    path("buzz/list", BuzzListView.as_view(), name="buzz-list"),
    path(
        "buzz/user=<slug:username>/list",
        UserBuzzListView.as_view(),
        name="user-buzz-list",
    ),
    path("buzz/create", CreateBuzzView.as_view(), name="create-buzz"),
    path("buzz/id=<int:buzzid>/detail", BuzzDetailView.as_view(), name="buzz-detail"),
    path("buzz/id=<int:buzzid>/upvote", UpvoteBuzzView.as_view(), name="upvote-buzz"),
    path(
        "buzz/id=<int:buzzid>/downvote",
        DownvoteBuzzView.as_view(),
        name="downvote-buzz",
    ),
    path("buzz/id=<int:buzzid>/edit", EditBuzzView.as_view(), name="edit-buzz"),
    path("buzz/id=<int:buzzid>/delete", DeleteBuzzView.as_view(), name="delete-buzz"),
]

rebuzz = [
    path("rebuzz/list", RebuzzListView.as_view(), name="rebuzz-list"),
    path(
        "rebuzz/user=<slug:username>/list",
        UserRebuzzListView.as_view(),
        name="user-rebuzz-list",
    ),
    path(
        "rebuzz/create/buzzid=<int:buzzid>",
        CreateRebuzzView.as_view(),
        name="create-buzz",
    ),
    path(
        "rebuzz/id=<int:rebuzzid>/detail",
        RebuzzDetailView.as_view(),
        name="rebuzz-detail",
    ),
    path(
        "rebuzz/id=<int:rebuzzid>/upvote",
        UpvoteRebuzzView.as_view(),
        name="upvote-rebuzz",
    ),
    path(
        "rebuzz/id=<int:rebuzzid>/downvote",
        DownvoteRebuzzView.as_view(),
        name="downvote-rebuzz",
    ),
    path("rebuzz/id=<int:rebuzzid>/edit", EditRebuzzView.as_view(), name="edit-rebuzz"),
    path(
        "rebuzz/id=<int:rebuzzid>/delete",
        DeleteRebuzzView.as_view(),
        name="delete-rebuzz",
    ),
]

urlpatterns = buzz + rebuzz
