from rest_framework import serializers

from bumblebee.buzzes.models import Buzz, BuzzImage
from bumblebee.core.exceptions import UnknownModelFieldsError
from bumblebee.buzzes.api.serializers.interaction_serializers import (
    BuzzInteractionsSerializer,
)

from .user_serializers import BuzzUserSerializer

######################################
##           RETRIEVE
######################################


class BuzzImageSerializer(serializers.ModelSerializer):
    """ """

    image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = BuzzImage
        fields = ["image"]


class ListBuzzImageSerializer(serializers.ModelSerializer):
    """ """

    image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = BuzzImage
        fields = ["image"]


class BuzzDetailSerializer(serializers.ModelSerializer):
    """ """

    buzzid = serializers.IntegerField(source="id")

    created_date = serializers.DateTimeField()
    edited_date = serializers.DateTimeField()
    edited = serializers.BooleanField()

    privacy = serializers.ChoiceField(choices=Buzz.PrivacyChoices.choices)

    content = serializers.CharField(help_text="Something in your mind? Post a buzz")
    location = serializers.CharField()
    flair = serializers.ListField(child=serializers.CharField())

    author = BuzzUserSerializer(many=False)
    images = ListBuzzImageSerializer(source="buzz_image", many=True, read_only=True)
    interaction = BuzzInteractionsSerializer(source="buzz_interaction", read_only=True)

    class Meta:
        model = Buzz
        fields = [
            "buzzid",
            "created_date",
            "edited_date",
            "edited",
            "privacy",
            "content",
            "location",
            "flair",
            "author",
            "images",
            "interaction",
        ]


######################################
##           CREATE
######################################


class CreateBuzzSerializer(serializers.ModelSerializer):
    """ """

    privacy = serializers.ChoiceField(
        required=False, choices=Buzz.PrivacyChoices.choices
    )
    content = serializers.CharField(
        required=False, help_text="Something in your mind? Post a buzz"
    )
    flair = serializers.ListField(child=serializers.CharField(), required=False)
    location = serializers.CharField(required=False)

    class Meta:
        model = Buzz
        fields = ["privacy", "content", "location", "flair"]


class EditBuzzSerializer(serializers.ModelSerializer):
    """ """

    privacy = serializers.ChoiceField(
        required=False, choices=Buzz.PrivacyChoices.choices
    )
    content = serializers.CharField(
        required=False, help_text="Something in your mind? Post a buzz"
    )
    location = serializers.CharField(required=False)
    flair = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Buzz
        fields = ["privacy", "content", "location", "flair"]

    def update_buzz(self, buzz_instance, **validated_data):
        """ """
        try:
            for key, value in validated_data.items():
                if buzz_instance.__dict__.__contains__(key):
                    if buzz_instance.__getattribute__(key) != value:
                        buzz_instance.__setattr__(key, value)
                else:
                    raise UnknownModelFieldsError(
                        key,
                        f"'{buzz_instance.__class__.__name__}' object has no model field called {key}",
                    )
            if buzz_instance.__getattribute__("edited") != True:
                buzz_instance.__setattr__("edited", True)

            buzz_instance.save()

        except UnknownModelFieldsError as error:
            print(error)
            raise error

        except Exception as error:
            print("ERROR @update_buzz\n", error)
            raise error


class BuzzListSerializer(serializers.Serializer):
    """ """

    buzzid = serializers.IntegerField(source="id")
    author = BuzzUserSerializer()
    created_date = serializers.DateTimeField()
    edited_date = serializers.DateTimeField()
    edited = serializers.BooleanField()
    privacy = serializers.CharField()
    content = serializers.CharField()
    location = serializers.CharField()
    flair = serializers.ListField()
    images = ListBuzzImageSerializer(source="buzz_image", many=True, read_only=True)
    interaction = BuzzInteractionsSerializer(source="buzz_interaction", read_only=True)

    class Meta:
        """ """

        model = Buzz
        fields = [
            "buzzid",
            "author",
            "created_date",
            "edited_date",
            "privacy",
            "content",
            "location",
            "flair",
            "images",
            "interaction",
        ]
        # depth = 1
