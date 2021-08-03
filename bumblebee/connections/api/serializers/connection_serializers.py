"""
Serializers for Connection
"""

from rest_framework import serializers

from bumblebee.comments.models import Comment
from bumblebee.connections.models import Blocked, Follower, Following, Muted
from bumblebee.core.exceptions import UnknownModelFieldsError

from .connection_users_serializers import ConnectionUserSerializer

######################################
##           RETRIEVE
######################################


class FollowerSerializer(serializers.ModelSerializer):
    """ """

    user = ConnectionUserSerializer(many=False)
    created_date = serializers.DateTimeField()
    follower = serializers.ListField(help_text="list of ids of users who follow you")

    class Meta:
        model = Follower
        fields = [
            "user",
            "created_date",
            "follower",
        ]


class FollowingSerializer(serializers.ModelSerializer):
    """ """

    user = ConnectionUserSerializer(many=False)
    created_date = serializers.DateTimeField()
    following = serializers.ListField(help_text="list of ids of users who you follow")

    class Meta:
        model = Following
        fields = [
            "user",
            "created_date",
            "following",
        ]


class MutedSerializer(serializers.ModelSerializer):
    """ """

    user = ConnectionUserSerializer(many=False)
    created_date = serializers.DateTimeField()
    muted = serializers.ListField(help_text="list of ids of users who you muted")

    class Meta:
        model = Muted
        fields = [
            "user",
            "created_date",
            "muted",
        ]


class BlockedSerializer(serializers.ModelSerializer):
    """ """

    user = ConnectionUserSerializer(many=False)
    created_date = serializers.DateTimeField()
    blocked = serializers.ListField(help_text="list of ids of users who you blocked")

    class Meta:
        model = Blocked
        fields = [
            "user",
            "created_date",
            "blocked",
        ]


######################################
##           CREATE
######################################


# class CreateFollowerSerializer(serializers.ModelSerializer):
#     """ """

#     follower = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Blocked
#         fields = [
#             "follower",
#         ]


# class CreateFollowingSerializer(serializers.ModelSerializer):
#     """ """

#     following = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Blocked
#         fields = [
#             "following",
#         ]


# class CreateBlockedSerializer(serializers.ModelSerializer):
#     """ """

#     blocked = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Blocked
#         fields = [
#             "blocked",
#         ]


# class CreateMutedSerializer(serializers.ModelSerializer):
#     """ """

#     muted = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Blocked
#         fields = [
#             "muted",
#         ]


# class CreateBlockedSerializer(serializers.ModelSerializer):
#     """ """

#     blocked = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Blocked
#         fields = [
#             "created_date",
#             "blocked",
#         ]
