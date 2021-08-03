from rest_framework import serializers

from bumblebee.buzzes.api.serializers.user_serializers import BuzzUserSerializer
from bumblebee.users.models import CustomUser


class NotificationOwnerSerializer(serializers.ModelSerializer):
    """ """

    userid = serializers.IntegerField(source="id")
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [
            "userid",
            "username",
        ]


class UserSerializer(BuzzUserSerializer):
    """ """

    pass
