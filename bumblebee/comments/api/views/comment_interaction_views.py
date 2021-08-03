from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.comments.utils import (
    create_comment_upvdwv_meta,
    delete_comment_upvdwv_meta,
    get_interactions_from_commentid_or_raise,
)
from bumblebee.core.exceptions import NoneExistenceError, UrlParameterError
from bumblebee.core.helpers import create_200, create_400, create_500
from bumblebee.core.permissions import IsBuzzPublic
from bumblebee.notifications.choices import ACTION_TYPE, CONTENT_TYPE
from bumblebee.notifications.utils import create_notification, delete_notification

########################################
##              COMMENT
########################################


class UpvoteCommentView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ """

        try:
            comment_interaction = get_interactions_from_commentid_or_raise(**kwargs)

            userid = request.user.id

            # check if already downvoted
            if userid in comment_interaction.downvotes:
                comment_interaction.downvotes.remove(userid)

                delete_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["CMNT"],
                    request.user,
                    comment_interaction.comment,
                )

            # check if already upvoted
            if userid not in comment_interaction.upvotes:
                comment_interaction.upvotes.append(userid)
                task = "Added UPVOTE"

                create_comment_upvdwv_meta(
                    userid=userid, comment_interaction=comment_interaction, action="UPV"
                )
                create_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["CMNT"],
                    request.user,
                    comment_interaction.comment,
                )

            else:
                comment_interaction.upvotes.remove(userid)
                task = "Removed UPVOTE"

                delete_comment_upvdwv_meta(
                    userid=userid, comment_interaction=comment_interaction, action="UPV"
                )
                delete_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["CMNT"],
                    request.user,
                    comment_interaction.comment,
                )

            comment_interaction.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"{task} on comment {{ id:{comment_interaction.comment.id}, commenter:{comment_interaction.comment.commenter.username} }}",
                ),
                status=status.HTTP_200_OK,
            )
        except (UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not upvote due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DownvoteCommentView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ """

        try:
            comment_interaction = get_interactions_from_commentid_or_raise(**kwargs)
            userid = request.user.id

            # check if already upvoted
            if userid in comment_interaction.upvotes:
                comment_interaction.upvotes.remove(userid)

                delete_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["CMNT"],
                    request.user,
                    comment_interaction.comment,
                )

            # check if already in downvoted
            if userid not in comment_interaction.downvotes:
                comment_interaction.downvotes.append(userid)
                task = "Added DOWNVOTE"

                create_comment_upvdwv_meta(
                    userid=userid, comment_interaction=comment_interaction, action="DWV"
                )
                create_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["CMNT"],
                    request.user,
                    comment_interaction.comment,
                )
            else:
                comment_interaction.downvotes.remove(userid)
                task = "Removed DOWNVOTE"

                delete_comment_upvdwv_meta(
                    userid=userid, comment_interaction=comment_interaction, action="DWV"
                )
                delete_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["CMNT"],
                    request.user,
                    comment_interaction.comment,
                )

            comment_interaction.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"{task} on comment {{ id:{comment_interaction.comment.id}, commenter:{comment_interaction.comment.commenter.username} }}",
                ),
                status=status.HTTP_200_OK,
            )
        except (UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not downvote due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
