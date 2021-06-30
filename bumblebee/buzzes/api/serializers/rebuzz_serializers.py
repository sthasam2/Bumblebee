from rest_framework import serializers

from bumblebee.buzzes.models import Rebuzz
from bumblebee.core.exceptions import UnknownModelFieldsError
from bumblebee.buzzes.api.serializers.interaction_serializers import (
    BuzzInteractionsSerializer,
)
from bumblebee.buzzes.api.serializers.buzz_serializers import (
    BuzzDetailSerializer,
    ListBuzzImageSerializer,
)

from .user_serializers import BuzzUserSerializer


class RebuzzDetailSerializer(serializers.ModelSerializer):
    """ """

    rebuzzid = serializers.IntegerField(source="id")

    created_date = serializers.DateTimeField()
    edited_date = serializers.DateTimeField()
    edited = serializers.BooleanField()

    privacy = serializers.ChoiceField(choices=Rebuzz.PrivacyChoices.choices)

    content = serializers.CharField(help_text="Something in your mind? Post a buzz")
    location = serializers.CharField()
    flair = serializers.ListField(child=serializers.CharField())

    author = BuzzUserSerializer(many=False)
    buzz = BuzzDetailSerializer(source="buzz_rebuzz", many=False)
    images = ListBuzzImageSerializer(source="buzz_image", many=True, read_only=True)
    interaction = BuzzInteractionsSerializer(source="buzz_interaction", read_only=True)

    class Meta:
        model = Rebuzz
        fields = [
            "rebuzzid",
            "created_date",
            "edited_date",
            "edited",
            "privacy",
            "content",
            "location",
            "flair",
            "author",
            "buzz",
            "images",
            "interaction",
        ]


class CreateRebuzzSerializer(serializers.ModelSerializer):
    """ """

    privacy = serializers.ChoiceField(
        required=False, choices=Rebuzz.PrivacyChoices.choices
    )
    content = serializers.CharField(
        required=False, help_text="Something in your mind? Post a buzz"
    )
    flair = serializers.ListField(child=serializers.CharField(), required=False)
    location = serializers.CharField(required=False)

    class Meta:
        model = Rebuzz
        fields = ["privacy", "content", "location", "flair"]


class EditRebuzzSerializer(serializers.ModelSerializer):
    """ """

    privacy = serializers.ChoiceField(
        required=False, choices=Rebuzz.PrivacyChoices.choices
    )
    content = serializers.CharField(
        required=False, help_text="Something in your mind? Post a buzz"
    )
    location = serializers.CharField(required=False)
    flair = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Rebuzz
        fields = ["privacy", "content", "location", "flair"]

    def update_rebuzz(self, rebuzz_instance, **validated_data):
        """ """
        try:
            for key, value in validated_data.items():
                if rebuzz_instance.__dict__.__contains__(key):
                    if rebuzz_instance.__getattribute__(key) != value:
                        rebuzz_instance.__setattr__(key, value)
                else:
                    raise UnknownModelFieldsError(
                        key,
                        f"'{rebuzz_instance.__class__.__name__}' object has no model field called {key}",
                    )
            if rebuzz_instance.__getattribute__("edited") != True:
                rebuzz_instance.__setattr__("edited", True)

            rebuzz_instance.save()

        except UnknownModelFieldsError as error:
            print(error)
            raise error

        except Exception as error:
            print("ERROR @update_buzz\n", error)
            raise error


class RebuzzListSerializer(serializers.Serializer):
    """ """

    rebuzzid = serializers.IntegerField(source="id")
    created_date = serializers.DateTimeField()
    edited_date = serializers.DateTimeField()
    edited = serializers.BooleanField()
    privacy = serializers.CharField()
    content = serializers.CharField()
    location = serializers.CharField()
    flair = serializers.ListField()

    author = BuzzUserSerializer()
    buzz = BuzzDetailSerializer(source="buzz_rebuzz", many=False)
    images = ListBuzzImageSerializer(source="buzz_image", many=True, read_only=True)
    interaction = BuzzInteractionsSerializer(source="buzz_interaction", read_only=True)

    class Meta:
        """ """

        model = Rebuzz
        fields = [
            "rebuzzid",
            "created_date",
            "edited_date",
            "privacy",
            "content",
            "location",
            "flair",
            "author",
            "buzz",
            "images",
            "interaction",
        ]
        # depth = 1
