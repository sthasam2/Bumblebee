from rest_framework import serializers

from bumblebee.comments.models import CommentInteractions


class CommentInteractionsSerializer(serializers.ModelSerializer):
    """ """

    commentid = serializers.PrimaryKeyRelatedField(
        source="buzz_interaction.id", read_only=True
    )

    upvote_ids = serializers.ListField(
        source="upvotes", help_text="list of ids of users who upvoted"
    )
    downvote_ids = serializers.ListField(
        source="downvotes", help_text="list of ids of users who downvoted"
    )
    reply_ids = serializers.ListField(
        source="replies", help_text="list of ids of comments"
    )

    upvoted_count = serializers.SerializerMethodField()
    downvoted_count = serializers.SerializerMethodField()
    replied_count = serializers.SerializerMethodField()

    class Meta:
        model = CommentInteractions
        fields = [
            "commentid",
            "upvote_ids",
            "downvote_ids",
            "reply_ids",
            "upvoted_count",
            "downvoted_count",
            "replied_count",
        ]

    def get_upvoted_count(self, obj):
        return len(obj.upvotes)

    def get_downvoted_count(self, obj):
        return len(obj.downvotes)

    def get_replied_count(self, obj):
        return len(obj.replies)
