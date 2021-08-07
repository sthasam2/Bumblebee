"""
Serializers for Buzz Notifications
"""

from rest_framework import serializers

from bumblebee.notifications.models.grouped_models import BuzzNotification
from bumblebee.notifications.models.individual_models import (
    CommentBuzzNotification,
    DownvoteBuzzNotification,
    RebuzzBuzzNotification,
    UpvoteBuzzNotification,
)
from bumblebee.notifications.api.serializers.user_serializers import UserSerializer

######################################
##           GROUPED
######################################


class BuzzNotificationDetailSerializer(serializers.ModelSerializer):
    """ """

    buzzid = serializers.IntegerField(source="buzz.id")

    updated_date = serializers.DateTimeField(
        source="buzz.buzz_interaction.updated_date"
    )

    upvote_notification = serializers.SerializerMethodField()
    downvote_notification = serializers.SerializerMethodField()
    rebuzz_notification = serializers.SerializerMethodField()
    comment_notification = serializers.SerializerMethodField()

    class Meta:
        model = BuzzNotification
        fields = [
            "buzzid",
            "updated_date",
            "upvote_notification",
            "downvote_notification",
            "rebuzz_notification",
            "comment_notification",
        ]

    def get_upvote_notification(self, obj):
        return obj.get_upvote_notification()

    def get_downvote_notification(self, obj):
        return obj.get_downvote_notification()

    def get_rebuzz_notification(self, obj):
        return obj.get_rebuzz_notification()

    def get_comment_notification(self, obj):
        return obj.get_rebuzz_notification()


class UpvoteBuzzNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Buzz")
    action = serializers.CharField(default="Upvote")
    buzzid = serializers.IntegerField(source="buzz.id")
    updated_date = serializers.DateTimeField(
        source="buzz.buzz_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = BuzzNotification
        fields = [
            "contenttype",
            "action",
            "buzzid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_upvote_notification()


class DownvoteBuzzNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Buzz")
    action = serializers.CharField(default="Downvote")
    buzzid = serializers.IntegerField(source="buzz.id")
    updated_date = serializers.DateTimeField(
        source="buzz.buzz_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = BuzzNotification
        fields = [
            "contenttype",
            "action",
            "buzzid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_downvote_notification()


class RebuzzBuzzNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Buzz")
    action = serializers.CharField(default="Rebuzz")
    buzzid = serializers.IntegerField(source="buzz.id")
    updated_date = serializers.DateTimeField(
        source="buzz.buzz_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = BuzzNotification
        fields = [
            "contenttype",
            "action",
            "buzzid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_rebuzz_notification()


class CommentBuzzNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Buzz")
    action = serializers.CharField(default="Comment")
    buzzid = serializers.IntegerField(source="buzz.id")
    updated_date = serializers.DateTimeField(
        source="buzz.buzz_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = BuzzNotification
        fields = [
            "contenttype",
            "action",
            "buzzid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_comment_notification()


#################################
#       INDIVIDUAL
#################################


class UpvoteBuzzIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    buzzid = serializers.IntegerField(source="buzz.id")
    contenttype = serializers.CharField(default="Buzz")
    action = serializers.CharField(default="Upvoted")
    timestamp = serializers.DateTimeField()

    agent = UserSerializer()
    notification = serializers.SerializerMethodField()

    class Meta:
        model = UpvoteBuzzNotification
        fields = [
            "buzzid",
            "contenttype",
            "action",
            "timestamp",
            "agent_username",
            "agent_id",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class DownvoteBuzzIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    buzzid = serializers.IntegerField(source="buzz.id")
    contenttype = serializers.CharField(default="Buzz")
    action = serializers.CharField(default="Downvoted")

    timestamp = serializers.DateTimeField()

    agent = UserSerializer()

    notification = serializers.SerializerMethodField()

    class Meta:
        model = DownvoteBuzzNotification
        fields = [
            "buzzid",
            "contenttype",
            "action",
            "timestamp",
            "agent_username",
            "agent_id",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class RebuzzBuzzIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    buzzid = serializers.IntegerField(source="buzz.id")
    contenttype = serializers.CharField(default="Buzz")
    action = serializers.CharField(default="Rebuzzed")

    timestamp = serializers.DateTimeField()

    agent = UserSerializer()

    notification = serializers.SerializerMethodField()

    class Meta:
        model = BuzzNotification
        fields = [
            "buzzid",
            "contenttype",
            "action",
            "timestamp",
            "agent_username",
            "agent_id",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class CommentBuzzIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    buzzid = serializers.IntegerField(source="buzz.id")
    contenttype = serializers.CharField(default="Buzz")
    action = serializers.CharField(default="Commented")

    timestamp = serializers.DateTimeField()

    agent = UserSerializer()

    notification = serializers.SerializerMethodField()

    class Meta:
        model = BuzzNotification
        fields = [
            "buzzid",
            "contenttype",
            "action",
            "timestamp",
            "agent_username",
            "agent_id",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()
