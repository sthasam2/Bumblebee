# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework_simplejwt.views import TokenObtainPairView

from bumblebee.core.helpers import create_400

from ..schemas import LoginAcceptedResponseSchema, Response400Schema, Response500Schema
from ..serializers import CustomTokenObtainPairSerializer

##################################
##          RETRIEVE
##################################


class CustomTokenObtainPairView(TokenObtainPairView):
    """ """

    serializer_class = CustomTokenObtainPairSerializer

    # @swagger_auto_schema(
    #     responses={
    #         HTTP_401_UNAUTHORIZED: openapi.Response(
    #             description="Access Denied", schema=Response400Schema
    #         ),
    #         HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
    #             description="Internal Error", schema=Response500Schema
    #         ),
    #         HTTP_200_OK: openapi.Response(
    #             description="Login Accepted", schema=LoginAcceptedResponseSchema
    #         ),
    #     },
    # )
    def post(self, request, *args, **kwargs):
        """
        POST method for jwt  tokens
        """

        context = super().post(request, *args, **kwargs)

        if not context.data["user_details"]["email_verified"]:

            return Response(
                data=create_400(401, "Access Denied!", "Email not verified!"),
                status=HTTP_401_UNAUTHORIZED,
            )
        else:
            return context
