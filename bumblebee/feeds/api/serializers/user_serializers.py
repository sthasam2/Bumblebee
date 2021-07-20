from rest_framework import serializers

from bumblebee.users.models import CustomUser


class FeedUserSerializer(serializers.ModelSerializer):
    """ """

    userid = serializers.IntegerField(source="id")
    username = serializers.CharField()
    account_verified = serializers.BooleanField(source="profile.account_verified")
    avatar = serializers.ImageField(source="profile.avatar")
    nickname = serializers.CharField(source="profile.nickname")

    class Meta:
        model = CustomUser
        fields = [
            "userid",
            "username",
            "account_verified",
            "avatar",
            "nickname",
        ]
