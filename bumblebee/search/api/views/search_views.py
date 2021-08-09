from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.buzzes.models import Buzz, Rebuzz
from bumblebee.core.exceptions import (
    ExtraFieldsError,
    NoneExistenceError,
    UrlParameterError,
)
from bumblebee.core.helpers import create_200, create_400, create_500
from bumblebee.users.models import CustomUser
from bumblebee.buzzes.api.serializers.buzz_serializers import BuzzDetailSerializer
from bumblebee.buzzes.api.serializers.rebuzz_serializers import RebuzzDetailSerializer
from bumblebee.search.api.serializers.user_serializers import SearchUserSerializer


class SearchView(APIView):
    """ """

    # serializer_class =
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ """
        try:
            keyword = self.request.query_params.get("keyword")

            if keyword is not None:
                buzzes = Buzz.objects.filter(
                    Q(content__icontains=keyword)
                    | Q(author__username__icontains=keyword)
                ).exclude(privacy="priv")
                rebuzzes = Rebuzz.objects.filter(
                    Q(content__icontains=keyword)
                    | Q(author__username__icontains=keyword)
                ).exclude(privacy="priv")
                users = CustomUser.objects.filter(Q(username__icontains=keyword))

                return dict(buzzes=buzzes, rebuzzes=rebuzzes, users=users)

            else:
                raise UrlParameterError(
                    "url",
                    create_400(
                        status.HTTP_400_BAD_REQUEST,
                        "Url Error",
                        "Query Params missing. either `keyword` or `username` must be provided",
                        "url:query params",
                    ),
                )
        except UrlParameterError as error:
            raise error

    def get(self, request, *args, **kwargs):
        """ """
        try:
            results = self.get_queryset()

            user_serializers = SearchUserSerializer(results["users"], many=True)
            buzz_serializers = BuzzDetailSerializer(results["buzzes"], many=True)
            rebuzz_serializers = RebuzzDetailSerializer(results["rebuzzes"], many=True)

            return Response(
                dict(
                    users=user_serializers.data,
                    buzzes=buzz_serializers.data,
                    rebuzzes=rebuzz_serializers.data,
                    users_count=len(user_serializers.data),
                    buzzes_count=len(buzz_serializers.data),
                    rebuzzes_count=len(rebuzz_serializers.data),
                ),
                status.HTTP_200_OK,
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
