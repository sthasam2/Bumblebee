from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.buzzes.models import Rebuzz
from bumblebee.buzzes.utils import (
    get_buzz_from_buzzid_or_raise,
    get_rebuzz_from_rebuzzid_or_raise,
    check_previously_rebuzzed,
)
from bumblebee.core.exceptions import (
    MissingFieldsError,
    NoneExistenceError,
    PreExistenceError,
    UrlParameterError,
)
from bumblebee.core.helpers import (
    RequestFieldsChecker,
    create_200,
    create_400,
    create_500,
)
from bumblebee.core.permissions import IsProfilePrivate, IsRebuzzOwner
from bumblebee.notifications.choices import ACTION_TYPE, CONTENT_TYPE
from bumblebee.notifications.utils import create_notification, delete_notification
from bumblebee.users.utils import DbExistenceChecker

from ..serializers.rebuzz_serializers import (
    CreateRebuzzSerializer,
    EditRebuzzSerializer,
    RebuzzDetailSerializer,
    RebuzzImageSerializer,
)

##################################
##          RETRIEVE            ##
##################################


class UserRebuzzListView(APIView):
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
                if self.request.user.id in user_instance.user_follower.follower:
                    return user_instance

                else:
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

    def _get_rebuzzes(self, *args, **kwargs):
        """ """

        user_instance = self._get_url_user()
        if self.request.user == user_instance:
            return user_instance.author_rebuzz.all()
        else:
            return user_instance.author_rebuzz.filter(privacy="pub")

    def get(self, request, *args, **kwargs):
        """ """

        try:
            rebuzz_instances = self._get_rebuzzes()
            rebuzz_serializer = RebuzzDetailSerializer(rebuzz_instances, many=True)

            return Response(
                rebuzz_serializer.data,
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
                    verbose=f"Could not get rebuzzes of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RebuzzListView(APIView):
    """
    Get a list of rebuzzes from a list of ids of rebuzzes
    """

    # TODO: Fix user profile private stuff
    permission_classes = [AllowAny]

    def _get_rebuzzes(self, *args, **kwargs):
        """ """
        rebuzzid_list = self.request.data.get("rebuzzid_list", False)

        if rebuzzid_list:
            rebuzzes = Rebuzz.objects.filter(id__in=rebuzzid_list)
            return dict(
                public=rebuzzes.filter(privacy="pub").all(),
                private=set(doc.id for doc in rebuzzes.filter(privacy="priv")),
                non_existing=(
                    set(rebuzzid_list) - set([rebuzz.id for rebuzz in rebuzzes.all()])
                ),
            )
        else:
            raise MissingFieldsError(
                "rebuzzid_list",
                create_400(
                    400,
                    "Missing Fields",
                    "Request body must contain field `buzzid_list`",
                ),
            )

    def post(self, request, *args, **kwargs):
        """ """

        try:
            rebuzz_instances = self._get_rebuzzes()
            rebuzz_serializer = RebuzzDetailSerializer(
                rebuzz_instances.get("public"), many=True
            )

            return Response(
                data=dict(
                    public=rebuzz_serializer.data,
                    private=rebuzz_instances.get("private"),
                    non_existing=rebuzz_instances.get("non_existing"),
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
                    verbose=f"Could not get details for `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RebuzzDetailView(APIView):
    """
    Get details of a rebuzz from rebuzzid
    """

    permission_classes = [AllowAny]

    def _get_rebuzz(self, request, *args, **kwargs):
        """
        Get Buzz from kwargs i.e. url
        """

        rebuzz = get_rebuzz_from_rebuzzid_or_raise(**kwargs)
        if rebuzz.privacy != "pub":
            raise PermissionDenied(
                detail="Rebuzz not Public",
                code="User has made not made their rebuzz public.",
            )
        else:
            return rebuzz

    def get(self, request, *args, **kwargs):
        """
        GET method for Rebuzz Detail API View
        """

        try:
            rebuzz_instance = self._get_rebuzz(request, **kwargs)
            serializer = RebuzzDetailSerializer(rebuzz_instance)

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


class CreateRebuzzView(APIView):
    """
    Create Rebuzz for Buzz of given id
    """

    serializer_class = CreateRebuzzSerializer
    permission_classes = [IsAuthenticated]

    def _check_referenced_buzz(self, *args, **kwargs):
        """
        Check the buzz from url
        """
        url_buzz = get_buzz_from_buzzid_or_raise(**kwargs)
        return url_buzz

    def _check_images(self, request):
        """
        check whether `images` are present in request.data
        """

        return request.data.__contains__("images")

    def _handle_rebuzz_images(self, request, created_rebuzz):
        """
        Handle images if image is present in request.data

        Note: returns an error if image is not present,
        so check for content or image before using
        if both not present it leads to error.
        """
        try:
            if not self._check_images(request):
                raise MissingFieldsError(
                    "request.data.images",
                    create_400(
                        400, "Missing Field", "Request body missing `images` field"
                    ),
                )

            for image in request.data.getlist("images"):
                rebuzz_image = RebuzzImageSerializer(data=dict(image=image))
                if rebuzz_image.is_valid(raise_exception=True):
                    rebuzz_image.save(
                        rebuzz=created_rebuzz, **rebuzz_image.validated_data
                    )

        except Exception as error:
            print("error @handle_buzz_image", error)
            raise error

    def _check_previously_rebuzzed(self, buzzid):
        """ """

        try:
            if check_previously_rebuzzed(user=self.request.user, buzzid=buzzid):
                raise PreExistenceError(
                    "rebuzz",
                    create_400(
                        400,
                        "Pre-existence of rebuzz",
                        "The given buzz has been previously rebuzzed. Cannot rebuzz again.",
                    ),
                )
        except Exception as error:
            print("error @check_previously_rebuzz", error)
            raise error

    def post(self, request, *args, **kwargs):
        """
        POST method for creating Rebuzz
        """

        try:
            data = request.data

            # check either image or content
            RequestFieldsChecker().check_at_least_one_field_or_raise(
                data, ["content", "images"]
            )
            referenced_buzz = self._check_referenced_buzz(**kwargs)

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            created_rebuzz = serializer.save(
                author=request.user, buzz=referenced_buzz, **serializer.validated_data
            )
            # handle images
            if data.__contains__("images"):
                self._handle_rebuzz_images(request, created_rebuzz)

            referenced_buzz.buzz_interaction.rebuzzes.append(created_rebuzz.id)
            referenced_buzz.buzz_interaction.save()

            # create notification
            create_notification(
                ACTION_TYPE["RBZ"],
                CONTENT_TYPE["BUZZ"],
                request.user,
                referenced_buzz,
                created_rebuzz,
            )

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Rebuzz Created",
                    f"Rebuzz created.\n {dict(rebuzzid=created_rebuzz.id, author=request.user.username, referenced_buzzid=referenced_buzz.id)}",
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
                    verbose=f"Could not create rebuzz due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


##################################
##          UPDATE
##################################


class EditRebuzzView(APIView):

    serializer_class = EditRebuzzSerializer
    permission_classes = [
        IsAuthenticated,
        IsRebuzzOwner,
    ]

    required_fields = None
    field_options = ["privacy", "content", "location", "flair"]

    def _get_rebuzz(self, *args, **kwargs):
        """
        Get Buzz from kwargs i.e. url
        """

        rebuzz = get_rebuzz_from_rebuzzid_or_raise(**kwargs)
        if rebuzz.author == self.request.user:
            return rebuzz
        else:
            raise PermissionDenied(
                detail="Rebuzz doesn't belong to requesting user",
                code="Rebuzz ownership mismatch",
            )

    def patch(self, request, *args, **kwargs):
        """ """

        try:
            data = request.data
            rebuzz_to_update = self._get_rebuzz(**kwargs)

            # check request fields
            RequestFieldsChecker().check_fields(
                data, self.field_options, self.required_fields
            )
            # check permissions for object
            self.check_object_permissions(request, rebuzz_to_update)

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.update_rebuzz(rebuzz_to_update, **serializer.validated_data)

            return Response(
                create_200(
                    status.HTTP_200_OK,
                    "Rebuzz Updated",
                    f"Rebuzz has been updated.",
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


class DeleteRebuzzView(APIView):
    """ """

    permission_classes = [
        IsAuthenticated,
        IsRebuzzOwner,
    ]

    def delete(self, request, *args, **kwargs):
        """ """

        try:
            rebuzz_to_delete = get_rebuzz_from_rebuzzid_or_raise(**kwargs)
            self.check_object_permissions(request, rebuzz_to_delete)

            rebuzz_to_delete_id = rebuzz_to_delete.id
            rebuzz_to_delete.delete()

            referenced_buzz = rebuzz_to_delete.buzz
            referenced_buzz.buzz_interaction.rebuzzes.remove(rebuzz_to_delete_id)
            referenced_buzz.buzz_interaction.save()

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
