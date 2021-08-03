from datetime import datetime as dt

from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.core.exceptions import (
    MissingFieldsError,
    NoneExistenceError,
    UrlParameterError,
)
from bumblebee.core.helpers import create_400, create_500
from bumblebee.notifications.api.serializers.buzz_notif_serializers import (
    CommentBuzzIndividualNotificationSerializer,
    DownvoteBuzzIndividualNotificationSerializer,
    RebuzzBuzzIndividualNotificationSerializer,
    UpvoteBuzzIndividualNotificationSerializer,
)
from bumblebee.notifications.api.serializers.comment_notif_serializers import (
    DownvoteCommentIndividualNotificationSerializer,
    ReplyCommentIndividualNotificationSerializer,
    UpvoteCommentIndividualNotificationSerializer,
)
from bumblebee.notifications.api.serializers.connection_notif_serializers import (
    NewFollowerNotificationSerializer,
    NewFollowerRequestNotificationSerializer,
    AcceptedFollowerRequestNotificationSerializer,
    RejectedFollowerRequestNotificationSerializer,
)
from bumblebee.notifications.api.serializers.rebuzz_notif_serializers import (
    CommentRebuzzIndividualNotificationSerializer,
    DownvoteRebuzzIndividualNotificationSerializer,
    UpvoteRebuzzIndividualNotificationSerializer,
)
from bumblebee.notifications.api.serializers.user_serializers import (
    NotificationOwnerSerializer,
)
from bumblebee.notifications.utils import get_individual_notifications_for_userid

##################################
##          RETRIEVE
##################################


class UserIndividualNotificationView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_notifications(self, *args, **kwargs):
        """ """

        return get_individual_notifications_for_userid(self.request.user.id)

    def get(self, request, *args, **kwargs):
        """ """
        try:

            user_serializer = NotificationOwnerSerializer(self.request.user)
            notification_instances = self._get_notifications()

            # buzz notifications
            buzz_upvote_notif_serialzier = UpvoteBuzzIndividualNotificationSerializer(
                notification_instances["buzz_notification"]["upvote_notification"],
                many=True,
            )
            buzz_downvote_notif_serialzier = (
                DownvoteBuzzIndividualNotificationSerializer(
                    notification_instances["buzz_notification"][
                        "downvote_notification"
                    ],
                    many=True,
                )
            )
            buzz_comment_notif_serialzier = CommentBuzzIndividualNotificationSerializer(
                notification_instances["buzz_notification"]["comment_notification"],
                many=True,
            )
            buzz_rebuzz_notif_serialzier = RebuzzBuzzIndividualNotificationSerializer(
                notification_instances["buzz_notification"]["rebuzz_notification"],
                many=True,
            )

            # rebuzz notification
            rebuzz_upvote_notif_serialzier = (
                UpvoteRebuzzIndividualNotificationSerializer(
                    notification_instances["rebuzz_notification"][
                        "upvote_notification"
                    ],
                    many=True,
                )
            )
            rebuzz_downvote_notif_serialzier = (
                DownvoteRebuzzIndividualNotificationSerializer(
                    notification_instances["rebuzz_notification"][
                        "downvote_notification"
                    ],
                    many=True,
                )
            )
            rebuzz_comment_notif_serialzier = (
                CommentRebuzzIndividualNotificationSerializer(
                    notification_instances["rebuzz_notification"][
                        "comment_notification"
                    ],
                    many=True,
                )
            )

            # comment notifications
            comment_upvote_notif_serialzier = (
                UpvoteCommentIndividualNotificationSerializer(
                    notification_instances["comment_notification"][
                        "upvote_notification"
                    ],
                    many=True,
                )
            )
            comment_downvote_notif_serialzier = (
                DownvoteCommentIndividualNotificationSerializer(
                    notification_instances["comment_notification"][
                        "downvote_notification"
                    ],
                    many=True,
                )
            )
            comment_reply_notif_serialzier = (
                ReplyCommentIndividualNotificationSerializer(
                    notification_instances["comment_notification"][
                        "reply_notification"
                    ],
                    many=True,
                )
            )

            # connection notifications
            new_follower_notif_serialzier = NewFollowerNotificationSerializer(
                notification_instances["connection_notification"][
                    "follower_notification"
                ],
                many=True,
            )
            new_follower_request_notif_serialzier = (
                NewFollowerRequestNotificationSerializer(
                    notification_instances["connection_notification"][
                        "follower_request_notification"
                    ],
                    many=True,
                )
            )
            new_follower_request_accept_notif_serialzier = (
                AcceptedFollowerRequestNotificationSerializer(
                    notification_instances["connection_notification"][
                        "follower_request_accept_notification"
                    ],
                    many=True,
                )
            )
            new_follower_request_reject_notif_serialzier = (
                RejectedFollowerRequestNotificationSerializer(
                    notification_instances["connection_notification"][
                        "follower_request_reject_notification"
                    ],
                    many=True,
                )
            )

            return Response(
                dict(
                    notif_received_date=dt.now(),
                    user=user_serializer.data,
                    buzz_notification=buzz_upvote_notif_serialzier.data
                    + buzz_downvote_notif_serialzier.data
                    + buzz_comment_notif_serialzier.data
                    + buzz_rebuzz_notif_serialzier.data,
                    rebuzz_notification=rebuzz_upvote_notif_serialzier.data
                    + rebuzz_downvote_notif_serialzier.data
                    + rebuzz_comment_notif_serialzier.data,
                    comment_notification=comment_upvote_notif_serialzier.data
                    + comment_downvote_notif_serialzier.data
                    + comment_reply_notif_serialzier.data,
                    connection_notification=new_follower_notif_serialzier.data
                    + new_follower_request_notif_serialzier.data
                    + new_follower_request_accept_notif_serialzier.data
                    + new_follower_request_reject_notif_serialzier.data,
                ),
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
                    verbose=f"Could not get notifications of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserIndividualNotificationListView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_notifications(self, *args, **kwargs):
        """ """

        return get_individual_notifications_for_userid(self.request.user.id)

    def get(self, request, *args, **kwargs):
        """ """
        try:

            user_serializer = NotificationOwnerSerializer(self.request.user)
            notification_instances = self._get_notifications()

            # buzz notifications
            buzz_upvote_notif_serialzier = UpvoteBuzzIndividualNotificationSerializer(
                notification_instances["buzz_notification"]["upvote_notification"],
                many=True,
            )
            buzz_downvote_notif_serialzier = (
                DownvoteBuzzIndividualNotificationSerializer(
                    notification_instances["buzz_notification"][
                        "downvote_notification"
                    ],
                    many=True,
                )
            )
            buzz_comment_notif_serialzier = CommentBuzzIndividualNotificationSerializer(
                notification_instances["buzz_notification"]["comment_notification"],
                many=True,
            )
            buzz_rebuzz_notif_serialzier = RebuzzBuzzIndividualNotificationSerializer(
                notification_instances["buzz_notification"]["rebuzz_notification"],
                many=True,
            )

            # rebuzz notification
            rebuzz_upvote_notif_serialzier = (
                UpvoteRebuzzIndividualNotificationSerializer(
                    notification_instances["rebuzz_notification"][
                        "upvote_notification"
                    ],
                    many=True,
                )
            )
            rebuzz_downvote_notif_serialzier = (
                DownvoteRebuzzIndividualNotificationSerializer(
                    notification_instances["rebuzz_notification"][
                        "downvote_notification"
                    ],
                    many=True,
                )
            )
            rebuzz_comment_notif_serialzier = (
                CommentRebuzzIndividualNotificationSerializer(
                    notification_instances["rebuzz_notification"][
                        "comment_notification"
                    ],
                    many=True,
                )
            )

            # comment notifications
            comment_upvote_notif_serialzier = (
                UpvoteCommentIndividualNotificationSerializer(
                    notification_instances["comment_notification"][
                        "upvote_notification"
                    ],
                    many=True,
                )
            )
            comment_downvote_notif_serialzier = (
                DownvoteCommentIndividualNotificationSerializer(
                    notification_instances["comment_notification"][
                        "downvote_notification"
                    ],
                    many=True,
                )
            )
            comment_reply_notif_serialzier = (
                ReplyCommentIndividualNotificationSerializer(
                    notification_instances["comment_notification"][
                        "reply_notification"
                    ],
                    many=True,
                )
            )

            # connection notifications
            new_follower_notif_serialzier = NewFollowerNotificationSerializer(
                notification_instances["connection_notification"][
                    "follower_notification"
                ],
                many=True,
            )
            new_follower_request_notif_serialzier = (
                NewFollowerRequestNotificationSerializer(
                    notification_instances["connection_notification"][
                        "follower_request_notification"
                    ],
                    many=True,
                )
            )
            new_follower_request_accept_notif_serialzier = (
                AcceptedFollowerRequestNotificationSerializer(
                    notification_instances["connection_notification"][
                        "follower_request_accept_notification"
                    ],
                    many=True,
                )
            )
            new_follower_request_reject_notif_serialzier = (
                RejectedFollowerRequestNotificationSerializer(
                    notification_instances["connection_notification"][
                        "follower_request_reject_notification"
                    ],
                    many=True,
                )
            )
            
            return Response(
                dict(
                    notif_received_date=dt.now(),
                    user=user_serializer.data,
                    notifications=buzz_upvote_notif_serialzier.data
                    + buzz_downvote_notif_serialzier.data
                    + buzz_comment_notif_serialzier.data
                    + buzz_rebuzz_notif_serialzier.data
                    + rebuzz_upvote_notif_serialzier.data
                    + rebuzz_downvote_notif_serialzier.data
                    + rebuzz_comment_notif_serialzier.data
                    + comment_upvote_notif_serialzier.data
                    + comment_downvote_notif_serialzier.data
                    + comment_reply_notif_serialzier.data
                    + new_follower_notif_serialzier.data
                    + new_follower_request_notif_serialzier.data 
                    + new_follower_request_accept_notif_serialzier.data
                    + new_follower_request_reject_notif_serialzier.data,
                ),
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
                    verbose=f"Could not get notifications of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
