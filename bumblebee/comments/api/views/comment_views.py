from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.buzzes.utils import (
    get_buzz_from_buzzid_or_raise,
    get_rebuzz_from_rebuzzid_or_raise,
)
from bumblebee.comments.utils import (
    get_comment_from_commentid_or_raise,
    get_comments_from_commentid_list,
)
from bumblebee.core.exceptions import (
    ExtraFieldsError,
    MissingFieldsError,
    NoneExistenceError,
    UrlParameterError,
)
from bumblebee.core.helpers import (
    RequestFieldsChecker,
    create_200,
    create_400,
    create_500,
)
from bumblebee.core.permissions import IsCommentOwner
from bumblebee.notifications.choices import ACTION_TYPE, CONTENT_TYPE
from bumblebee.notifications.utils import create_notification, delete_notification

from ..serializers.comment_serializers import (
    CommentDetailSerializer,
    CreateCommentSerializer,
    EditCommentSerializer,
)

##################################
##          RETRIEVE
##################################


class BuzzOrRebuzzCommentListView(APIView):
    """
    Get comments and interactions for a given buzz
    """

    permission_classes = [AllowAny]

    def _get_url_buzz(self, url_buzzid):
        """ """

        if url_buzzid:
            buzz_instance = get_buzz_from_buzzid_or_raise(buzzid=url_buzzid)

            if buzz_instance.author.profile.private:
                raise PermissionDenied(
                    detail="Private Profile",
                    code="User has made their profile private.",
                )

            return buzz_instance

        else:
            raise UrlParameterError(
                "buzzid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `buzz id`",
                ),
            )

    def _get_url_rebuzz(self, url_rebuzzid):
        """ """

        if url_rebuzzid:
            rebuzz_instance = get_rebuzz_from_rebuzzid_or_raise(rebuzzid=url_rebuzzid)

            if rebuzz_instance.author.profile.private:
                raise PermissionDenied(
                    detail="Private Profile",
                    code="User has made their profile private.",
                )

            return rebuzz_instance

        else:
            raise UrlParameterError(
                "buzz or rebuzzid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `rebuzz id`",
                ),
            )

    def _get_comments(self, *args, **kwargs):
        """ """
        url_buzzid = self.kwargs.get("buzzid", False)
        url_rebuzzid = self.kwargs.get("rebuzzid", False)

        if url_buzzid:
            buzz_instance = self._get_url_buzz(url_buzzid)
            return buzz_instance.buzz_comment.filter(level=1)

        elif url_rebuzzid:
            rebuzz_instance = self._get_url_rebuzz(url_rebuzzid)
            return rebuzz_instance.rebuzz_comment.filter(level=1)

    def get(self, request, *args, **kwargs):
        """ """

        try:
            comment_instances = self._get_comments()
            comment_serializer = CommentDetailSerializer(comment_instances, many=True)

            return Response(
                comment_serializer.data,
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
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
                    verbose=f"Could not get buzzes of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CommentReplyListView(APIView):
    """
    Get comments and interactions for a given buzz
    """

    permission_classes = [AllowAny]

    def _get_url_comment(self, url_commentid):
        """ """

        if url_commentid:
            comment_instance = get_comment_from_commentid_or_raise(
                commentid=url_commentid
            )

            # if comment_instance.parent_buzz:
            #     if comment_instance.parent_buzz.author.profile.private:
            #         raise PermissionDenied(
            #             detail="Private Profile",
            #             code="User has made their profile private.",
            #         )

            # elif comment_instance.parent_buzz:
            #     if comment_instance.parent_rebuzz.author.profile.private:
            #         raise PermissionDenied(
            #             detail="Private Profile",
            #             code="User has made their profile private.",
            #         )

            # if comment_instance.parent_buzz:
            #     if comment_instance.parent_buzz.privacy == "priv":
            #         raise PermissionDenied(
            #             detail="Private Buzz",
            #             code="User has made their buzz private.",
            #         )
            # elif comment_instance.parent_buzz:
            #     if comment_instance.parent_rebuzz.privacy == "priv":
            #         raise PermissionDenied(
            #             detail="Private ReBuzz",
            #             code="User has made their rebuzz private.",
            #         )

            return comment_instance

        else:
            raise UrlParameterError(
                "commentid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `comment id`",
                ),
            )

    def _get_replies(self, *args, **kwargs):
        """ """
        url_commentid = self.kwargs.get("commentid", False)

        if url_commentid:
            comment_instance = self._get_url_comment(url_commentid)
            replyid_list = comment_instance.comment_interaction.replies

            if len(replyid_list) != 0:
                replies = get_comments_from_commentid_list(replyid_list)
                objects = replies["comments"].filter(level=comment_instance.level + 1)
                return objects

            else:
                return None

    def get(self, request, *args, **kwargs):
        """ """

        try:
            comment_instances = self._get_replies()
            comment_serializer = CommentDetailSerializer(comment_instances, many=True)

            return Response(
                comment_serializer.data,
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
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
                    verbose=f"Could not get buzzes of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CommentDetailView(APIView):
    """ """

    permission_classes = [AllowAny]

    def _get_url_comment(self, **kwargs):
        """ """
        url_commentid = self.kwargs.get("commentid", False)

        if url_commentid:
            comment_instance = get_comment_from_commentid_or_raise(
                commentid=url_commentid
            )

            # if comment_instance.parent_buzz.author.profile.private:
            #     raise PermissionDenied(
            #         detail="Private Profile",
            #         code="User has made their profile private.",
            #     )

            # if comment_instance.parent_buzz.privacy == "priv":
            #     raise PermissionDenied(
            #         detail="Private Buzz",
            #         code="User has made their buzz private.",
            #     )

            return comment_instance

        else:
            raise UrlParameterError(
                "commentid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `comment id`",
                ),
            )

    def get(self, request, *args, **kwargs):
        """ """

        try:
            comment_instance = self._get_url_comment(**kwargs)
            serializer = CommentDetailSerializer(comment_instance)

            return Response(
                serializer.data,
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
                    verbose=f"Could not get details for comment `id: {kwargs.get('commentid')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ##################################
# ##          CREATE
# ##################################


class CreateCommentView(APIView):
    """ """

    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def _get_url_buzz(self, url_buzzid):
        """ """

        if url_buzzid:
            buzz_instance = get_buzz_from_buzzid_or_raise(buzzid=url_buzzid)

            if buzz_instance.author.profile.private:
                raise PermissionDenied(
                    detail="Private Profile",
                    code="User has made their profile private.",
                )
            if buzz_instance.privacy == "priv":
                raise PermissionDenied(
                    detail="Private Buzz",
                    code="User has made their buzz private.",
                )

            return buzz_instance

        else:
            raise UrlParameterError(
                "buzzid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `buzz id`",
                ),
            )

    def _get_url_rebuzz(self, url_rebuzzid):
        """ """

        if url_rebuzzid:
            rebuzz_instance = get_rebuzz_from_rebuzzid_or_raise(rebuzzid=url_rebuzzid)

            if rebuzz_instance.author.profile.private:
                raise PermissionDenied(
                    detail="Private Profile",
                    code="User has made their profile private.",
                )
            if rebuzz_instance.privacy == "priv":
                raise PermissionDenied(
                    detail="Private Rebuzz",
                    code="User has made their rebuzz private.",
                )

            return rebuzz_instance

        else:
            raise UrlParameterError(
                "buzz or rebuzzid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `rebuzz id`",
                ),
            )

    def post(self, request, *args, **kwargs):
        """ """

        try:
            data = request.data

            # check either image or content
            RequestFieldsChecker().check_at_least_one_field_or_raise(
                data, ["content", "images"]
            )

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            url_buzzid = self.kwargs.get("buzzid", False)
            url_rebuzzid = self.kwargs.get("rebuzzid", False)

            if url_buzzid:
                buzz_instance = self._get_url_buzz(url_buzzid)
                created_comment = serializer.save(
                    commenter=request.user,
                    parent_buzz=buzz_instance,
                    level=1,
                    **serializer.validated_data,
                )
                interaction = buzz_instance.buzz_interaction
                interaction.comments.append(created_comment.id)

                # create notification
                create_notification(
                    ACTION_TYPE["CMNT"],
                    CONTENT_TYPE["BUZZ"],
                    request.user,
                    buzz_instance,
                    created_comment,
                )

            elif url_rebuzzid:
                rebuzz_instance = self._get_url_rebuzz(url_rebuzzid)
                created_comment = serializer.save(
                    commenter=request.user,
                    parent_rebuzz=rebuzz_instance,
                    **serializer.validated_data,
                )
                interaction = rebuzz_instance.rebuzz_interaction
                interaction.comments.append(created_comment.id)

                # create notification
                create_notification(
                    ACTION_TYPE["CMNT"],
                    CONTENT_TYPE["RBZ"],
                    request.user,
                    rebuzz_instance,
                    created_comment,
                )

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Comment Created",
                    f"Comment created.\n {dict(commentid=created_comment.id, commenter=request.user.username)}",
                ),
                status=status.HTTP_200_OK,
            )

        except (UrlParameterError, NoneExistenceError, MissingFieldsError) as error:
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
                    verbose=f"Could not create comment due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CreateCommentReplyView(APIView):
    """ """

    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def _get_url_comment(self, *args, **kwargs):
        """ """
        url_commentid = self.kwargs.get("commentid", False)
        if url_commentid:
            comment_instance = get_comment_from_commentid_or_raise(
                commentid=url_commentid
            )

            if comment_instance.parent_buzz:
                if comment_instance.parent_buzz.author.profile.private:
                    raise PermissionDenied(
                        detail="Private Profile",
                        code="User has made their profile private.",
                    )

                if comment_instance.parent_buzz.privacy == "priv":
                    raise PermissionDenied(
                        detail="Private Buzz",
                        code="User has made their buzz private.",
                    )

            elif comment_instance.parent_rebuzz:
                if comment_instance.parent_rebuzz.author.profile.private:
                    raise PermissionDenied(
                        detail="Private Profile",
                        code="User has made their profile private.",
                    )

                if comment_instance.parent_rebuzz.privacy == "priv":
                    raise PermissionDenied(
                        detail="Private Rebuzz",
                        code="User has made their rebuzz private.",
                    )

            return comment_instance

        else:
            raise UrlParameterError(
                "commentid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `comment id`",
                ),
            )

    def post(self, request, *args, **kwargs):
        """ """

        try:
            data = request.data

            RequestFieldsChecker().check_at_least_one_field_or_raise(
                data, ["content", "images"]
            )

            parent_comment = self._get_url_comment(**kwargs)

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            created_comment = serializer.save(
                commenter=request.user,
                parent_buzz=parent_comment.parent_buzz,
                parent_rebuzz=parent_comment.parent_rebuzz,
                parent_comment=parent_comment.id,
                level=parent_comment.level + 1,
                **serializer.validated_data,
            )

            parent_comment.comment_interaction.replies.append(created_comment.id)
            parent_comment.comment_interaction.save()

            # create notification
            create_notification(
                ACTION_TYPE["RPLY"],
                CONTENT_TYPE["CMNT"],
                request.user,
                parent_comment,
                created_comment,
            )

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Comment Created",
                    f"Comment created.\n {dict(commentid=created_comment.id, commenter=request.user.username)}",
                ),
                status=status.HTTP_200_OK,
            )

        except (UrlParameterError, NoneExistenceError, MissingFieldsError) as error:
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
                    verbose=f"Could not create comment due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ##################################
# ##          UPDATE
# ##################################


class EditCommentView(APIView):

    serializer_class = EditCommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsCommentOwner,
    ]

    required_fields = ["content"]
    field_options = ["content", "flair"]

    def _get_url_comment(self, *args, **kwargs):
        """ """
        url_commentid = self.kwargs.get("commentid", False)
        if url_commentid:
            comment_instance = get_comment_from_commentid_or_raise(
                commentid=url_commentid
            )

            # if comment_instance.parent_buzz:
            #     if comment_instance.parent_buzz.author.profile.private:
            #         raise PermissionDenied(
            #             detail="Private Profile",
            #             code="User has made their profile private.",
            #         )

            # elif comment_instance.parent_rebuzz:
            #     if comment_instance.parent_rebuzz.author.profile.private:
            #         raise PermissionDenied(
            #             detail="Private Profile",
            #             code="User has made their profile private.",
            #         )

            # if comment_instance.parent_buzz:
            #     if comment_instance.parent_buzz.privacy == "priv":
            #         raise PermissionDenied(
            #             detail="Private Buzz",
            #             code="User has made their buzz private.",
            #         )
            # elif comment_instance.parent_buzz:
            #     if comment_instance.parent_rebuzz.privacy == "priv":
            #         raise PermissionDenied(
            #             detail="Private ReBuzz",
            #             code="User has made their rebuzz private.",
            #         )

            return comment_instance

        else:
            raise UrlParameterError(
                "commentid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `comment id`",
                ),
            )

    def patch(self, request, *args, **kwargs):
        """ """

        try:
            data = request.data

            comment_to_update = self._get_url_comment(**kwargs)

            RequestFieldsChecker().check_fields(
                data, self.field_options, self.required_fields
            )

            self.check_object_permissions(request, comment_to_update)

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.update_comment(
                comment_to_update, edited=True, **serializer.validated_data
            )

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Comment Updated",
                    f"Comment has been updated. `id:{comment_to_update.id}`",
                ),
                status=status.HTTP_200_OK,
            )

        except (ExtraFieldsError, UrlParameterError, NoneExistenceError) as error:
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
                    verbose=f"Could not edit comment due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ##################################
# ##          DELETE
# ##################################


class DeleteCommentView(APIView):

    serializer_class = EditCommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsCommentOwner,
    ]

    def _get_url_comment(self, *args, **kwargs):
        """ """
        url_commentid = self.kwargs.get("commentid", False)
        if url_commentid:
            comment_instance = get_comment_from_commentid_or_raise(
                commentid=url_commentid
            )

            return comment_instance

        else:
            raise UrlParameterError(
                "commentid",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `comment id`",
                ),
            )

    def delete(self, request, *args, **kwargs):
        """ """

        try:

            comment_to_delete = self._get_url_comment(**kwargs)
            self.check_object_permissions(request, comment_to_delete)
            comment_to_delete.delete()

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Comment Deleted",
                    f"Comment has been deleted. `id:{comment_to_delete.id}`",
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
                    verbose=f"Could not delete comment due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
