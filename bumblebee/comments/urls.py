"""
comment-crud
comment-list
comment-detail
"""

from django.urls import path

from bumblebee.comments.api.views.comment_interaction_views import (
    DownvoteCommentView,
    UpvoteCommentView,
)
from bumblebee.comments.api.views.comment_views import (
    BuzzOrRebuzzCommentListView,
    CommentDetailView,
    CommentReplyListView,
    CreateCommentReplyView,
    CreateCommentView,
    DeleteCommentView,
    EditCommentView,
)

urlpatterns = [
    path(
        "id=<int:commentid>/detail",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
    path(
        "id=<int:commentid>/reply/list",
        CommentReplyListView.as_view(),
        name="comment-reply-list",
    ),
    path(
        "buzz/id=<int:buzzid>/create",
        CreateCommentView.as_view(),
        name="create-buzz-comment",
    ),
    path(
        "rebuzz/id=<int:rebuzzid>/create",
        CreateCommentView.as_view(),
        name="create-rebuzz-comment",
    ),
    path(
        "id=<int:commentid>/reply/create",
        CreateCommentReplyView.as_view(),
        name="create-comment-reply",
    ),
    path(
        "id=<int:commentid>/edit",
        EditCommentView.as_view(),
        name="edit-comment",
    ),
    path(
        "id=<int:commentid>/delete",
        DeleteCommentView.as_view(),
        name="delete-comment",
    ),
    # interaction
    path(
        "id=<int:commentid>/upvote", UpvoteCommentView.as_view(), name="upvote-comment"
    ),
    path(
        "id=<int:commentid>/downvote",
        DownvoteCommentView.as_view(),
        name="downvote-comment",
    ),
    # buzz
    path(
        "buzz/id=<int:buzzid>/list",
        BuzzOrRebuzzCommentListView.as_view(),
        name="buzz-comment-list",
    ),
    # rebuzz
    path(
        "rebuzz/id=<int:rebuzzid>/list",
        BuzzOrRebuzzCommentListView.as_view(),
        name="rebuzz-comment-list",
    ),
]
