from django.db.models.fields import EmailField
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Model Serializer for creating CustomUser model
    """

    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text="Username. example: sam_smith",
        style={"input_type": "text", "placeholder": "Username"},
    )
    email = serializers.EmailField(
        max_length=150,
        required=True,
        help_text="Email address. example: example@example.domain",
        style={"input_type": "email", "placeholder": "Email"},
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="New password for ",
        style={"input_type": "password", "placeholder": "Password"},
    )

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


class SendEmailVerificationSerializer(serializers.Serializer):
    """ """

    email = serializers.EmailField(help_text="Email for verification resend")


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


class LogoutSerializer(serializers.Serializer):
    """ """

    refresh_token = serializers.CharField(
        help_text="Refresh token used for obtaining access token"
    )


class SendResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=150,
        required=True,
        help_text="Email address of account for resetting password",
        style={"input_type": "email", "placeholder": "Email"},
    )


class ConfirmResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=150,
        required=True,
        help_text="Email address of account for resetting password",
        style={"input_type": "email", "placeholder": "Email"},
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="New password for given user",
        style={"input_type": "password", "placeholder": "Password"},
    )
    token = serializers.CharField(
        max_length=150,
        required=True,
        help_text="Token for resetting password sent in the mail",
        style={"input_type": "text", "placeholder": "Token"},
    )
