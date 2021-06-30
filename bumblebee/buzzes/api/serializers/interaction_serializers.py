from rest_framework import serializers

from bumblebee.buzzes.models import BuzzInteractions


class BuzzInteractionsSerializer(serializers.ModelSerializer):
    """ """

    buzzid = serializers.PrimaryKeyRelatedField(
        source="buzz_interaction.id", read_only=True
    )
    views = serializers.IntegerField()
    upvote_ids = serializers.ListField(
        source="upvotes", help_text="list of ids of users who upvoted"
    )
    downvote_ids = serializers.ListField(
        source="downvotes", help_text="list of ids of users who downvoted"
    )
    comments = serializers.ListField(help_text="list of ids of comments")

    class Meta:
        model = BuzzInteractions
        fields = [
            "buzzid",
            "views",
            "upvote_ids",
            "downvote_ids",
            "comments",
        ]


class RebuzzInteractionsSerializer(serializers.ModelSerializer):
    """ """

    rebuzzid = serializers.PrimaryKeyRelatedField(
        source="rebuzz_interaction.id", read_only=True
    )
    views = serializers.IntegerField()
    upvote_ids = serializers.ListField(
        source="upvotes", help_text="list of ids of users who upvoted"
    )
    downvote_ids = serializers.ListField(
        source="downvotes", help_text="list of ids of users who downvoted"
    )
    comments = serializers.ListField(help_text="list of ids of comments")

    class Meta:
        model = BuzzInteractions
        fields = [
            "buzzid",
            "views",
            "upvote_ids",
            "downvote_ids",
            "comments",
        ]
