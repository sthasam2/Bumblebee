"""
Serializers for Connection Notifications
"""

from rest_framework import serializers

from bumblebee.notifications.api.serializers.user_serializers import UserSerializer
from bumblebee.notifications.models.individual_models import (
    NewFollowerNotification,
    NewFollowerRequestNotification,
)

######################################
##           RETRIEVE
######################################


class NewFollowerNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Connection")
    action = serializers.CharField(default="Follow")
    timestamp = serializers.DateTimeField()
    follower = UserSerializer()
    notification = serializers.SerializerMethodField()

    class Meta:
        model = NewFollowerNotification
        fields = [
            "contenttype",
            "action",
            "timestamp",
            "follower",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class NewFollowerRequestNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Connection")
    action = serializers.CharField(default="Request Follow")
    timestamp = serializers.DateTimeField()
    follower_requester = UserSerializer()
    notification = serializers.SerializerMethodField()

    class Meta:
        model = NewFollowerRequestNotification
        fields = [
            "contenttype",
            "action",
            "timestamp",
            "follower_requester",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class AcceptedFollowerRequestNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Connection")
    action = serializers.CharField(default="Accepted Request Follow")
    timestamp = serializers.DateTimeField()
    follower_requester = UserSerializer()
    notification = serializers.SerializerMethodField()

    class Meta:
        model = NewFollowerRequestNotification
        fields = [
            "contenttype",
            "action",
            "timestamp",
            "follower_requester",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()


class RejectedFollowerRequestNotificationSerializer(serializers.ModelSerializer):
    """ """

    contenttype = serializers.CharField(default="Connection")
    action = serializers.CharField(default="Rejected Request Follow")
    timestamp = serializers.DateTimeField()
    follower_requester = UserSerializer()
    notification = serializers.SerializerMethodField()

    class Meta:
        model = NewFollowerRequestNotification
        fields = [
            "contenttype",
            "action",
            "timestamp",
            "follower_requester",
            "notification",
        ]

    def get_notification(self, obj):
        return obj.__str__()
