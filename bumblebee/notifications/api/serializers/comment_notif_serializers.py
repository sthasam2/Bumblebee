"""
Serializers for Comment Notifications
"""

from rest_framework import serializers

from bumblebee.notifications.models.grouped_models import CommentNotification
from bumblebee.notifications.models.individual_models import (
    DownvoteCommentNotification,
    ReplyCommentNotification,
    UpvoteCommentNotification,
)
from bumblebee.notifications.api.serializers.user_serializers import UserSerializer

######################################
##           RETRIEVE
######################################


class CommentNotificationDetailSerializer(serializers.ModelSerializer):
    """ """

    commentid = serializers.IntegerField(source="comment.id")

    updated_date = serializers.DateTimeField(
        source="comment.comment_interaction.updated_date"
    )

    upvote_notification = serializers.SerializerMethodField()
    downvote_notification = serializers.SerializerMethodField()
    reply_notification = serializers.SerializerMethodField()

    class Meta:
        model = CommentNotification
        fields = [
            "commentid",
            "updated_date",
            "upvote_notification",
            "downvote_notification",
            "reply_notification",
        ]

    def get_upvote_notification(self, obj):
        return obj.get_upvote_notification()

    def get_downvote_notification(self, obj):
        return obj.get_downvote_notification()

    def get_reply_notification(self, obj):
        return obj.get_reply_notification()


class UpvoteCommentNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Comment")
    action = serializers.CharField(default="Upvote")
    commentid = serializers.IntegerField(source="comment.id")
    updated_date = serializers.DateTimeField(
        source="comment.comment_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = CommentNotification
        fields = [
            "contenttype",
            "action",
            "commentid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_upvote_notification()


class DownvoteCommentNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Comment")
    action = serializers.CharField(default="Downvote")
    commentid = serializers.IntegerField(source="comment.id")
    updated_date = serializers.DateTimeField(
        source="comment.comment_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = CommentNotification
        fields = [
            "contenttype",
            "action",
            "commentid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_downvote_notification()


class ReplyCommentNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Comment")
    action = serializers.CharField(default="Reply")
    commentid = serializers.IntegerField(source="comment.id")
    updated_date = serializers.DateTimeField(
        source="comment.comment_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = CommentNotification
        fields = [
            "contenttype",
            "action",
            "commentid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_reply_notification()


#######################################################
#               INDIVIDUAL
#######################################################


class UpvoteCommentIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    commentid = serializers.IntegerField(source="comment.id")
    contenttype = serializers.CharField(default="Comment")
    action = serializers.CharField(default="Upvoted")
    timestamp = serializers.DateTimeField()

    agent = UserSerializer()
    notification = serializers.SerializerMethodField()

    class Meta:
        model = UpvoteCommentNotification
        fields = [
            "commentid",
            "contenttype",
            "action",
            "timestamp",
            "agent",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class DownvoteCommentIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    commentid = serializers.IntegerField(source="comment.id")
    contenttype = serializers.CharField(default="Comment")
    action = serializers.CharField(default="Downvoted")

    timestamp = serializers.DateTimeField()

    agent = UserSerializer()

    notification = serializers.SerializerMethodField()

    class Meta:
        model = DownvoteCommentNotification
        fields = [
            "commentid",
            "contenttype",
            "action",
            "timestamp",
            "agent",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class ReplyCommentIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    commentid = serializers.IntegerField(source="comment.id")
    contenttype = serializers.CharField(default="Comment")
    action = serializers.CharField(default="Replied")

    timestamp = serializers.DateTimeField()

    agent = UserSerializer()

    notification = serializers.SerializerMethodField()

    class Meta:
        model = ReplyCommentNotification
        fields = [
            "commentid",
            "contenttype",
            "action",
            "timestamp",
            "agent",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()
