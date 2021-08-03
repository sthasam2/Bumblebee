"""
Serializers for Rebuzz Notifications
"""

from rest_framework import serializers

from bumblebee.notifications.models.grouped_models import RebuzzNotification
from bumblebee.notifications.models.individual_models import (
    CommentRebuzzNotification,
    DownvoteRebuzzNotification,
    UpvoteRebuzzNotification,
)

######################################
##           RETRIEVE
######################################


class RebuzzNotificationDetailSerializer(serializers.ModelSerializer):
    """ """

    rebuzzid = serializers.IntegerField(source="rebuzz.id")

    updated_date = serializers.DateTimeField(
        source="rebuzz.rebuzz_interaction.updated_date"
    )

    upvote_notification = serializers.SerializerMethodField()
    downvote_notification = serializers.SerializerMethodField()
    comment_notification = serializers.SerializerMethodField()

    class Meta:
        model = RebuzzNotification
        fields = [
            "rebuzzid",
            "updated_date",
            "upvote_notification",
            "downvote_notification",
            "comment_notification",
        ]

    def get_upvote_notification(self, obj):
        return obj.get_upvote_notification()

    def get_downvote_notification(self, obj):
        return obj.get_downvote_notification()

    def get_comment_notification(self, obj):
        return obj.get_rebuzz_notification()


class UpvoteRebuzzNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Rebuzz")
    action = serializers.CharField(default="Upvote")
    rebuzzid = serializers.IntegerField(source="rebuzz.id")
    updated_date = serializers.DateTimeField(
        source="rebuzz.rebuzz_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = RebuzzNotification
        fields = [
            "contenttype",
            "action",
            "rebuzzid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_upvote_notification()


class DownvoteRebuzzNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Rebuzz")
    action = serializers.CharField(default="Downvote")
    rebuzzid = serializers.IntegerField(source="rebuzz.id")
    updated_date = serializers.DateTimeField(
        source="rebuzz.rebuzz_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = RebuzzNotification
        fields = [
            "contenttype",
            "action",
            "rebuzzid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_downvote_notification()


class CommentRebuzzNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Rebuzz")
    action = serializers.CharField(default="Comment")
    rebuzzid = serializers.IntegerField(source="rebuzz.id")
    updated_date = serializers.DateTimeField(
        source="rebuzz.rebuzz_interaction.updated_date"
    )
    notification = serializers.SerializerMethodField()

    class Meta:
        model = RebuzzNotification
        fields = [
            "contenttype",
            "action",
            "rebuzzid",
            "updated_date",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.get_comment_notification()


#######################################################
#               INDIVIDUAL
#######################################################


class UpvoteRebuzzIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    rebuzzid = serializers.IntegerField(source="rebuzz.id")
    contenttype = serializers.CharField(default="Rebuzz")
    action = serializers.CharField(default="Comment")
    timestamp = serializers.DateTimeField()
    agent_username = serializers.CharField(source="agent.username")
    agent_id = serializers.CharField(source="agent.id")
    notification = serializers.SerializerMethodField()

    class Meta:
        model = UpvoteRebuzzNotification
        fields = [
            "rebuzzid",
            "contenttype",
            "action",
            "timestamp",
            "agent_username",
            "agent_id",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class DownvoteRebuzzIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    rebuzzid = serializers.IntegerField(source="rebuzz.id")
    contenttype = serializers.CharField(default="Rebuzz")
    action = serializers.CharField(default="Comment")

    timestamp = serializers.DateTimeField()

    agent_username = serializers.CharField(source="agent.username")
    agent_id = serializers.CharField(source="agent.id")

    notification = serializers.SerializerMethodField()

    class Meta:
        model = DownvoteRebuzzNotification
        fields = [
            "rebuzzid",
            "contenttype",
            "action",
            "timestamp",
            "agent_username",
            "agent_id",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class CommentRebuzzIndividualNotificationSerializer(serializers.ModelSerializer):
    """ """

    rebuzzid = serializers.IntegerField(source="rebuzz.id")
    contenttype = serializers.CharField(default="Rebuzz")
    action = serializers.CharField(default="Comment")

    timestamp = serializers.DateTimeField()

    agent_username = serializers.CharField(source="agent.username")
    agent_id = serializers.CharField(source="agent.id")

    notification = serializers.SerializerMethodField()

    class Meta:
        model = CommentRebuzzNotification
        fields = [
            "rebuzzid",
            "contenttype",
            "action",
            "timestamp",
            "agent_username",
            "agent_id",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()
