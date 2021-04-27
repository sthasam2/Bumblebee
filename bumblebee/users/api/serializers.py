from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Model Serializer for creating CustomUser model
    """

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password",
        ]

    def create(self, validated_data):
        """
        Creates a user instance in the database using valiadted fields

        Disclaimer: Please use validated data!
        """

        created_user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return created_user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializers for CustomUser model
    """

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ """

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        """
        serializer validate method
        """

        data = super().validate(attrs)

        data["user_details"] = dict(
            username=self.user.username,
            email=self.user.email,
            id=self.user.id,
            email_verified=self.user.email_verified,
        )

        return data
