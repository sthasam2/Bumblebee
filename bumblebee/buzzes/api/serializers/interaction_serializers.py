from rest_framework import serializers

from bumblebee.buzzes.models import BuzzInteractions


class BuzzInteractionsSerializer(serializers.ModelSerializer):
    """ """

    buzzid = serializers.PrimaryKeyRelatedField(source="buzz.id", read_only=True)
    upvote_ids = serializers.ListField(
        source="upvotes", help_text="list of ids of users who upvoted"
    )
    downvote_ids = serializers.ListField(
        source="downvotes", help_text="list of ids of users who downvoted"
    )
    comment_ids = serializers.ListField(
        source="comments", help_text="list of ids of comments"
    )
    rebuzz_ids = serializers.ListField(
        source="rebuzzes", help_text="list of ids of rebuzzes"
    )

    upvoted_count = serializers.SerializerMethodField()
    downvoted_count = serializers.SerializerMethodField()
    commented_count = serializers.SerializerMethodField()
    rebuzzed_count = serializers.SerializerMethodField()

    class Meta:
        model = BuzzInteractions
        fields = [
            "buzzid",
            "upvote_ids",
            "downvote_ids",
            "comment_ids",
            "rebuzz_ids",
            "upvoted_count",
            "downvoted_count",
            "commented_count",
            "rebuzzed_count",
        ]

    def get_upvoted_count(self, obj):
        return len(obj.upvotes)

    def get_downvoted_count(self, obj):
        return len(obj.downvotes)

    def get_commented_count(self, obj):
        return len(obj.comments)

    def get_rebuzzed_count(self, obj):
        return len(obj.rebuzzes)


class RebuzzInteractionsSerializer(serializers.ModelSerializer):
    """ """

    rebuzzid = serializers.PrimaryKeyRelatedField(source="rebuzz.id", read_only=True)
    upvote_ids = serializers.ListField(
        source="upvotes", help_text="list of ids of users who upvoted"
    )
    downvote_ids = serializers.ListField(
        source="downvotes", help_text="list of ids of users who downvoted"
    )
    comment_ids = serializers.ListField(
        source="comments", help_text="list of ids of comments"
    )
    upvoted_count = serializers.SerializerMethodField()
    downvoted_count = serializers.SerializerMethodField()
    commented_count = serializers.SerializerMethodField()

    class Meta:
        model = BuzzInteractions
        fields = [
            "buzzid",
            "upvote_ids",
            "downvote_ids",
            "comment_ids",
            "upvoted_count",
            "downvoted_count",
            "commented_count",
        ]

    def get_upvoted_count(self, obj):
        return len(obj.upvotes)

    def get_downvoted_count(self, obj):
        return len(obj.downvotes)

    def get_commented_count(self, obj):
        return len(obj.comments)
