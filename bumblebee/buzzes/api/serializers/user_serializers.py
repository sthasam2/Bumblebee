from rest_framework import serializers

from bumblebee.users.models import CustomUser


class BuzzUserSerializer(serializers.ModelSerializer):
    """ """

    userid = serializers.IntegerField(source="id")
    username = serializers.CharField()
    account_verified = serializers.BooleanField(source="profile.account_verified")
    avatar = serializers.ImageField(source="profile.avatar")
    cover = serializers.ImageField(source="profile.cover")
    nickname = serializers.CharField(source="profile.nickname")

    class Meta:
        model = CustomUser
        fields = [
            "userid",
            "username",
            "account_verified",
            "avatar",
            "cover",
            "nickname",
        ]


# class ProfileMetaSerializer
