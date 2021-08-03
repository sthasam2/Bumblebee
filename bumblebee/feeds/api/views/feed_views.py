import datetime as dt

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
from bumblebee.feeds.api.serializers.feed_serializers import (
    FeedBuzzSerializer,
    FeedRebuzzSerializer,
)
from bumblebee.feeds.api.serializers.user_serializers import FeedUserSerializer
from bumblebee.feeds.utils import (
    get_follow_suggestions_for_user,
    get_folowing_buzzes_for_user,
)
from bumblebee.users.utils import DbExistenceChecker


class FeedBuzzListView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def get_posts(self, *args, **kwargs):
        """ """

        return get_folowing_buzzes_for_user(self.request.user)

    def get(self, request, *args, **kwargs):
        """ """

        try:

            post_instances = self.get_posts()
            user_serializer = FeedUserSerializer(self.request.user, many=False)
            buzz_serializer = FeedBuzzSerializer(
                post_instances.get("buzzes"), many=True
            )
            rebuzz_serializer = FeedRebuzzSerializer(
                post_instances.get("rebuzzes"), many=True
            )

            return Response(
                data=dict(
                    updated_time=dt.datetime.now(),
                    user=user_serializer.data,
                    post=buzz_serializer.data + rebuzz_serializer.data,
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
                    verbose=f"Could not get feed due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FeedFollowSuggestionsListView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def get_suggestions(self, *args, **kwargs):
        """ """

        return get_follow_suggestions_for_user(self.request.user)

    def get(self, request, *args, **kwargs):
        """ """

        try:
            suggestion_instances = self.get_suggestions()
            user_serializer = FeedUserSerializer(self.request.user, many=False)
            suggestion_serializer = FeedUserSerializer(suggestion_instances, many=True)

            return Response(
                data=dict(
                    updated_time=dt.datetime.now(),
                    user=user_serializer.data,
                    suggestions=suggestion_serializer.data,
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
                    verbose=f"Could not get suggestions due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
