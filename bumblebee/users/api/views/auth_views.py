from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from bumblebee.users.exceptions import (
    AlreadyEmailVerifiedError,
    ExpiredError,
    MissingFieldsError,
    NoneExistenceError,
    PreExistenceError,
    UnmatchedFieldsError,
)
from bumblebee.users.models import CustomUser, EmailToken
from bumblebee.users.utils import DbExistenceChecker, EmailSender

from ..helpers import (
    create_200_response_dict,
    create_400_response_dict,
    create_general_exception_response_dict,
)
from ..serializers import (
    ConfirmResetPasswordSerializer,
    CreateUserSerializer,
    LogoutSerializer,
    SendEmailVerificationSerializer,
    SendResetPasswordSerializer,
)
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
        request.query_params
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
                            status.HTTP_400_BAD_REQUEST,
                            "Already exists",
                            f'User with email "{email}" already exists. Try a different email',
                        ),
                    )

                if checker.check_username_existence(username):
                    raise PreExistenceError(
                        username,
                        create_400_response_dict(
                            status.HTTP_400_BAD_REQUEST,
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
                    status=status.HTTP_201_CREATED,
                )
            else:
                raise MissingFieldsError(
                    instance=request,
                    message=create_400_response_dict(
                        status.HTTP_400_BAD_REQUEST,
                        "Missing Fields",
                        "Either of the required fields email, username, and/or password is missing.",
                    ),
                )

        except (MissingFieldsError, PreExistenceError) as error:
            return Response(error.message, status=error.message["status"])

        except Exception as error:
            return Response(
                create_general_exception_response_dict(
                    500,
                    "Internal Error",
                    f"Could not create account due to an unknown error.",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyEmailView(APIView):
    """ """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        GET method for email activation
        """
        try:
            # get token and username
            uid = force_text(urlsafe_base64_decode(kwargs["uidb64"]))
            token = kwargs["token"]

            # check token and user existence
            checker = DbExistenceChecker()

            try:
                user_to_verify = checker.check_return_user_existence(pk=uid)
            except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                raise NoneExistenceError(
                    "User",
                    create_400_response_dict(
                        400,
                        "Non existence",
                        "User associated to token does not exist",
                    ),
                )

            try:
                email_token = checker.check_return_token_existence(token=token)
            except (TypeError, ValueError, OverflowError, EmailToken.DoesNotExist):
                raise NoneExistenceError(
                    "Email Token",
                    create_400_response_dict(
                        400,
                        "Non existence",
                        "Token does not exist",
                    ),
                )

            # check expired
            if email_token.check_expired:
                raise ExpiredError(
                    "Email Token",
                    create_400_response_dict(
                        400, "Expired", "Email Token already expired!"
                    ),
                )

            # check token user and uid match
            if email_token.user.id != user_to_verify.id:
                raise UnmatchedFieldsError(
                    "User",
                    create_400_response_dict(
                        400, "Not matching", "Url user and Token user don't match!"
                    ),
                )

            user_to_verify.email_verified = True
            user_to_verify.save()

            return Response(
                create_200_response_dict(
                    200,
                    "Email verified",
                    "Email has been verified. Now you can login to your account",
                )
            )

        except (NoneExistenceError, ExpiredError, UnmatchedFieldsError) as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response(
                create_general_exception_response_dict(
                    500,
                    "Internal Error",
                    f"Could not verify due to an unknown error.",
                    error.args[0],
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ResendEmailVerificationView(APIView):
    """ """

    permission_classes = [AllowAny]
    serializer_class = SendEmailVerificationSerializer

    @swagger_auto_schema(
        # responses={
        #     status.HTTP_401_UNAUTHORIZED: openapi.Response(
        #         description="Access Denied", schema=Response400Schema
        #     ),
        #     status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
        #         description="Internal Error", schema=Response500Schema
        #     ),
        #     status.HTTP_200_OK: openapi.Response(
        #         description="Login Accepted", schema=LoginAcceptedResponseSchema
        #     ),
        # },
    )
    def post(self, request, *args, **kwargs):
        """ """
        try:
            # TODO  check last sent verification and dont allow multiple email in certain timeframe

            email = request.data.get("email", False)
            if email:

                checker = DbExistenceChecker()
                try:
                    user_requested = checker.check_return_user_existence(email=email)
                except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                    raise NoneExistenceError(
                        email,
                        create_400_response_dict(
                            400,
                            "Non existence",
                            f"Account with email {email} credentials does not exist! Check email or sign up using a different email",
                        ),
                    )

                if not user_requested.email_verified:
                    email_sender = EmailSender()
                    email_sender.send_email_verification_mail(request, user_requested)

                    return Response(
                        create_200_response_dict(
                            202,
                            "Email Sent",
                            f'A new verification email has been sent to email"{email}"!',
                        ),
                        status=status.HTTP_202_ACCEPTED,
                    )
                else:
                    raise AlreadyEmailVerifiedError(
                        message=create_400_response_dict(
                            400,
                            "Already verified",
                            "`email` already verified.",
                        ),
                    )

            else:
                raise MissingFieldsError(
                    instance=request,
                    message=create_400_response_dict(
                        status.HTTP_400_BAD_REQUEST,
                        "Missing fields",
                        "`email` field is mandatory. Please provide email",
                    ),
                )

        except (
            AlreadyEmailVerifiedError,
            MissingFieldsError,
            NoneExistenceError,
        ) as error:
            return Response(error.message, status=error.message["status"])

        except Exception as error:
            return Response(
                create_general_exception_response_dict(
                    500,
                    "Internal Error",
                    f"Could not send verification email due to an unknown error.",
                    error.args[0],
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(CustomTokenObtainPairView):
    """ """

    permission_classes = [AllowAny]


class LogoutView(APIView):
    """ """

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        """ """

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                create_200_response_dict(202, "Logged out", "Sucessfully logged out"),
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                create_400_response_dict(400, "Error occuored", e.args[0]),
                status=status.HTTP_400_BAD_REQUEST,
            )


class SendResetPasswordView(APIView):
    """ """

    permission_classes = [AllowAny]
    serializer_class = SendResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        """ """
        try:
            # TODO  check last sent verification and dont allow multiple email in certain timeframe

            email = request.data.get("email", False)
            if email:

                checker = DbExistenceChecker()
                try:
                    user_requested = checker.check_return_user_existence(email=email)

                except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                    raise NoneExistenceError(
                        email,
                        create_400_response_dict(
                            400,
                            "Non existence",
                            f"Account with email {email} credentials does not exist!",
                        ),
                    )

                email_sender = EmailSender()
                email_sender.send_password_reset_email(request, user_requested)

                return Response(
                    create_200_response_dict(
                        202,
                        "Email Sent",
                        f'A new password email has been sent to email"{email}"!',
                    ),
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                raise MissingFieldsError(
                    instance=request,
                    message=create_400_response_dict(
                        status.HTTP_400_BAD_REQUEST,
                        "Missing fields",
                        "`email` field is mandatory. Please provide email",
                    ),
                )

        except (
            AlreadyEmailVerifiedError,
            MissingFieldsError,
            NoneExistenceError,
        ) as error:
            return Response(error.message, status=error.message["status"])

        except Exception as error:
            return Response(
                create_general_exception_response_dict(
                    500,
                    "Internal Error",
                    f"Could not send reset account password email due to an unknown error.",
                    error.args[0],
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ConfirmResetPasswordView(APIView):
    """ """

    permission_classes = [AllowAny]
    serializer_class = ConfirmResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        """
        POST method for email activation
        """
        try:
            # get token , email, password
            email = request.data.get("email", False)
            token = request.data.get("token", False)
            password = request.data.get("password", False)

            if email and token and password:
                checker = DbExistenceChecker()

                try:
                    user_to_reset = checker.check_return_user_existence(email=email)
                except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                    raise NoneExistenceError(
                        "User",
                        create_400_response_dict(
                            400,
                            "Non existence",
                            "User associated to token does not exist",
                        ),
                    )
                try:
                    email_token = checker.check_return_token_existence(token=token)
                except (TypeError, ValueError, OverflowError, EmailToken.DoesNotExist):
                    raise NoneExistenceError(
                        "Email Token",
                        create_400_response_dict(
                            400,
                            "Non existence",
                            "Token does not exist",
                        ),
                    )

                # check expired
                if email_token.check_expired:
                    raise ExpiredError(
                        "Email Token",
                        create_400_response_dict(
                            400, "Expired", "Email Token already expired!"
                        ),
                    )

                # check token user and uid match
                if email_token.user.id != user_to_reset.id:
                    raise UnmatchedFieldsError(
                        "User",
                        create_400_response_dict(
                            400, "Not matching", "Url user and Token user don't match!"
                        ),
                    )

                user_to_reset.set_password(password)
                user_to_reset.save()

                return Response(
                    create_200_response_dict(
                        200,
                        "Password Resetted!",
                        "Password has been resetted. Now you can login to your account",
                    )
                )
            else:
                raise MissingFieldsError(
                    instance=request,
                    message=create_400_response_dict(
                        status.HTTP_400_BAD_REQUEST,
                        "Missing fields",
                        "Either of the required fileds: email, password, and/or token missing",
                    ),
                )
        except (MissingFieldsError, NoneExistenceError, ExpiredError) as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response(
                create_general_exception_response_dict(
                    500,
                    "Internal Error",
                    f"Could not reset password due to an unknown error.",
                    error.args[0],
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
