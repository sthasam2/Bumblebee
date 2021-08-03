from django.db.models import Q
from rest_framework import status

from bumblebee.comments.models import (
    Comment,
    CommentInteractions,
    CommentUpvoteDownvoteMeta,
)
from bumblebee.core.exceptions import (
    MissingFieldsError,
    NoneExistenceError,
    UrlParameterError,
)
from bumblebee.core.helpers import create_400


def get_comment_from_commentid_or_raise(**kwargs):
    """ """

    url_commentid = kwargs.get("commentid", False)
    if url_commentid:
        try:
            return Comment.objects.get(id=url_commentid)

        except (TypeError, ValueError, OverflowError, Comment.DoesNotExist):
            raise NoneExistenceError(
                url_commentid,
                create_400(
                    400,
                    "Non existence",
                    f"Comment with `id: {url_commentid}` credentials does not exist!",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Commentid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`commentid` must be provided",
            ),
        )


def get_comments_from_commentid_list(commentid_list):
    """ """

    if commentid_list:
        comments = Comment.objects.filter(id__in=commentid_list)
        return dict(
            comments=comments,
            non_existing=(
                set(commentid_list) - set([comment.id for comment in comments.all()])
            ),
        )


def get_interactions_from_commentid_or_raise(**kwargs):
    """ """

    url_commentid = kwargs.get("commentid", False)
    if url_commentid:
        try:
            return CommentInteractions.objects.get(comment__id=url_commentid)

        except (TypeError, ValueError, OverflowError, CommentInteractions.DoesNotExist):
            raise NoneExistenceError(
                url_commentid,
                create_400(
                    400,
                    "Non existence",
                    f"Comment with `id: {url_commentid}` credentials does not exist!",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Commentid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`commentid` must be provided",
            ),
        )


def create_comment_upvdwv_meta(comment_interaction, userid, action):
    """ """

    if action == "UPV":

        CommentUpvoteDownvoteMeta.objects.create(
            comment_interaction=comment_interaction,
            userid=userid,
            action=CommentUpvoteDownvoteMeta.ActionChoices.UPVOTE,
        )
    elif action == "DWV":
        CommentUpvoteDownvoteMeta.objects.create(
            comment_interaction=comment_interaction,
            userid=userid,
            action=CommentUpvoteDownvoteMeta.ActionChoices.DOWNVOTE,
        )


def delete_comment_upvdwv_meta(comment_interaction, userid, action):
    """ """

    if action == "UPV":
        meta = CommentUpvoteDownvoteMeta.objects.get(
            Q(comment_interaction=comment_interaction),
            Q(userid=userid),
            Q(action=CommentUpvoteDownvoteMeta.ActionChoices.UPVOTE),
        )
        if meta:
            meta.delete()
    elif action == "DWV":
        meta = CommentUpvoteDownvoteMeta.objects.get(
            Q(comment_interaction=comment_interaction),
            Q(userid=userid),
            Q(action=CommentUpvoteDownvoteMeta.ActionChoices.DOWNVOTE),
        )
        if meta:
            meta.delete()
