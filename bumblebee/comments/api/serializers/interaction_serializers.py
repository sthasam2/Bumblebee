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
    replies = serializers.ListField(help_text="list of ids of comments")

    class Meta:
        model = CommentInteractions
        fields = [
            "commentid",
            "upvote_ids",
            "downvote_ids",
            "replies",
        ]
