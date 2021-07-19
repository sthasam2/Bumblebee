from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.buzzes.models import Buzz
from bumblebee.buzzes.utils import get_buzz_from_buzzid_or_raise
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
from bumblebee.core.permissions import IsBuzzOwner, IsProfilePrivate
from bumblebee.users.utils import DbExistenceChecker

from ..serializers.buzz_serializers import (
    BuzzDetailSerializer,
    BuzzImageSerializer,
    CreateBuzzSerializer,
    EditBuzzSerializer,
)

##################################
##          RETRIEVE
##################################


class UserBuzzListView(APIView):
    """ """

    permission_classes = [AllowAny]

    def _get_url_user(self):
        """ """
        url_username = self.kwargs.get("username", False)

        if url_username:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=url_username
            )

            if user_instance.profile.private:
                raise PermissionDenied(
                    detail="Private Profile",
                    code="User has made their profile private.",
                )

            return user_instance
        else:
            raise UrlParameterError(
                "username",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `username`",
                ),
            )

    def _get_buzzes(self, *args, **kwargs):
        """ """

        user_instance = self._get_url_user()
        if self.request.user == user_instance:
            return user_instance.author_buzz.all()
        else:
            return user_instance.author_buzz.filter(privacy="pub")

    def get(self, request, *args, **kwargs):
        """ """

        try:
            buzz_instances = self._get_buzzes()
            buzz_serializer = BuzzDetailSerializer(buzz_instances, many=True)

            return Response(
                buzz_serializer.data,
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


class BuzzListView(APIView):
    """ """

    permission_classes = [AllowAny]

    def get_buzzes(self, *args, **kwargs):
        """ """
        buzzid_list = self.request.data.get("buzzid_list", False)

        if buzzid_list:
            buzzes = Buzz.objects.filter(id__in=buzzid_list)
            return dict(
                public=buzzes.filter(privacy="pub").all(),
                private=set(doc.id for doc in buzzes.filter(privacy="priv")),
                non_existing=(
                    set(buzzid_list) - set([buzz.id for buzz in buzzes.all()])
                ),
            )
        else:
            raise MissingFieldsError(
                "buzzid_list",
                create_400(
                    400,
                    "Missing Fields",
                    "Request body must contain field `buzzid_list`",
                ),
            )

    def post(self, request, *args, **kwargs):
        """ """

        try:

            buzz_instances = self.get_buzzes()
            buzz_serializer = BuzzDetailSerializer(
                buzz_instances.get("public"), many=True
            )

            return Response(
                data=dict(
                    public=buzz_serializer.data,
                    private=buzz_instances.get("private"),
                    non_existing=buzz_instances.get("non_existing"),
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
                    verbose=f"Could not get buzzes of list due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BuzzDetailView(APIView):
    """
    Get Buzz Detail View
    """

    permission_classes = [AllowAny]

    def _get_buzz(self, *args, **kwargs):
        """Get Buzz"""
        url_buzz = get_buzz_from_buzzid_or_raise(**kwargs)
        if url_buzz.privacy != "pub":
            raise PermissionDenied(
                detail="Buzz not Public",
                code="User has made not made their buzz public.",
            )
        else:
            return url_buzz

    def get(self, request, *args, **kwargs):
        """ """

        try:
            buzz_instance = self._get_buzz(**kwargs)
            serializer = BuzzDetailSerializer(buzz_instance)

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
                    verbose=f"Could not get details for `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


##################################
##          CREATE
##################################


class CreateBuzzView(APIView):
    """
    Create a Buzz


    Method
    ---
    post:
    - body => {
        "content" : (1000 char),
        "images" : (max 8),
        "privacy" : (3 options: -priv, -pub, -prot),
        "location" : (500 char),
        "flair" : (array)
    }
    """

    serializer_class = CreateBuzzSerializer
    permission_classes = [IsAuthenticated]
    field_options = ["content", "images", "privacy", "location", "flair"]

    def _check_images(self, request):
        """ """

        return request.data.__contains__("images")

    def _handle_buzz_images(self, request, created_buzz):
        """ """
        try:
            if not self._check_images(request):
                raise MissingFieldsError(
                    "request.data.images",
                    create_400(
                        400, "Missing Field", "Request body missing `images` field"
                    ),
                )

            if len(request.data.getlist("images")) > 8:
                raise ExtraFieldsError(
                    "request.data.images",
                    create_400(
                        400,
                        "Extra Field Data",
                        "Request body `images` field provided with more than 8 images. 8 is the limit",
                    ),
                )

            for image in request.data.getlist("images"):
                buzz_image = BuzzImageSerializer(data=dict(image=image))
                if buzz_image.is_valid(raise_exception=True):
                    buzz_image.save(buzz=created_buzz, **buzz_image.validated_data)

        except Exception as error:
            print("error @handle_buzz_image", error)
            raise error

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

            created_buzz = serializer.save(
                author=request.user, **serializer.validated_data
            )
            # handle images
            if data.__contains__("images"):
                self._handle_buzz_images(request, created_buzz)

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Buzz Created",
                    f"Buzz created.\n {dict(buzzid=created_buzz.id, author=request.user.username)}",
                ),
                status=status.HTTP_200_OK,
            )

        except (
            UrlParameterError,
            NoneExistenceError,
            MissingFieldsError,
            ExtraFieldsError,
        ) as error:
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
                    verbose=f"Could not create buzz due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


##################################
##          UPDATE
##################################


class EditBuzzView(APIView):
    """
    Edit Buzz

    Methods
    ---
    patch:
    - body => {
        "content" : (1000 char),
        "privacy" : (3 options: -priv, -pub, -prot),
        "location" : (500 char),
        "flair" : (array)
    }
    """

    serializer_class = EditBuzzSerializer
    permission_classes = [
        IsAuthenticated,
        IsBuzzOwner,
    ]

    required_fields = None
    field_options = ["privacy", "content", "location", "flair"]

    def patch(self, request, *args, **kwargs):
        """ """

        try:
            data = request.data

            buzz_to_update = get_buzz_from_buzzid_or_raise(**kwargs)
            RequestFieldsChecker().check_fields(
                data, self.field_options, self.required_fields
            )
            self.check_object_permissions(request, buzz_to_update)

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.update_buzz(buzz_to_update, **serializer.validated_data)

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Buzz Updated",
                    f"Buzz has been updated.",
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
                    verbose=f"Could not update Buzz due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


##################################
##          DELETE
##################################


class DeleteBuzzView(APIView):
    """ """

    permission_classes = [
        IsAuthenticated,
        IsBuzzOwner,
    ]

    def delete(self, request, *args, **kwargs):
        """ """

        try:
            buzz_to_delete = get_buzz_from_buzzid_or_raise(**kwargs)
            self.check_object_permissions(request, buzz_to_delete)
            buzz_to_delete.delete()

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Buzz Deleted",
                    f"Buzz has been deleted.",
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
                    verbose=f"Could not delete Buzz due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
