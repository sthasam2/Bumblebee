from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from bumblebee.users.api.helpers import create_400_response_dict

from ..serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """ """

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        POST method for jwt  tokens
        """
        context = super().post(request, *args, **kwargs)

        if not context.data["user_details"]["email_verified"]:

            return Response(
                data=create_400_response_dict(
                    401, "Access Denied!", "Email not verified!"
                ),
                status=HTTP_401_UNAUTHORIZED,
            )
        else:
            return context
