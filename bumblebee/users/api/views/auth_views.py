"""
REGISTER
LOGIN
LOGOUT
SEND ACTIVATION EMAIL
ACTIVATE
PASSWORD RESET REQUEST
PASSWORD RESET CONFIRMATION
UPDATE
DELETE
"""


from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView

from bumblebee.users.exceptions import PreExistenceError
from bumblebee.users.utils import DbExistenceChecker, EmailSender

from ..helpers import (
    create_200_response_dict,
    create_400_response_dict,
    create_general_exception_response_dict,
)
from ..serializers import CreateUserSerializer
from .jwt_views import CustomTokenObtainPairView


class RegisterView(CreateAPIView):
    """
    General API View for registering users
    """

    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def get(self, request, *args, **kwargs):
        """
        Register GET method
        """
        return Response(
            dict(status=200, message="Register GET Page! Register an account here!")
        )

    def post(self, request, *args, **kwargs):
        """
        Register POST method
        """
        try:
            email = request.data.get("email", False)
            username = request.data.get("username", False)
            password = request.data.get("password", False)

            if email and username and password:

                checker = DbExistenceChecker()

                if checker.check_email_existence(email):
                    raise PreExistenceError(
                        email,
                        create_400_response_dict(
                            400,
                            "Already exists",
                            f'User with email "{email}" already exists. Try a different email',
                        ),
                    )

                if checker.check_username_existence(username):
                    raise PreExistenceError(
                        username,
                        create_400_response_dict(
                            400,
                            "Already exists",
                            f'User with username "{username}" already exists. Try a different username',
                        ),
                    )

                serializer = CreateUserSerializer(
                    data={"email": email, "username": username, "password": password}
                )
                serializer.is_valid(raise_exception=True)
                new_user = serializer.save()

                email_sender = EmailSender()
                email_sender.send_email_verification_mail(request, new_user)

                return Response(
                    create_200_response_dict(
                        201,
                        "Created",
                        f'A user account with email"{email}" and username "{username}" created!',
                    ),
                    status=HTTP_201_CREATED,
                )

        except PreExistenceError as error:
            return Response(error.message, status=HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response(
                create_general_exception_response_dict(
                    500,
                    "Internal Error",
                    f"Could not create account due to an unknown error.",
                ),
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


# class UserList(ListAPIView):
#     """
#     View for getting User List
#     """


class ActivateView(APIView):
    """ """

    permission_classes = [AllowAny]


class LoginView(CustomTokenObtainPairView):
    """ """

    permission_classes = [AllowAny]
