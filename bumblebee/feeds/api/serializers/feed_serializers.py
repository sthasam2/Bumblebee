from rest_framework import serializers

from bumblebee.buzzes.api.serializers.buzz_serializers import BuzzDetailSerializer
from bumblebee.buzzes.api.serializers.rebuzz_serializers import RebuzzDetailSerializer


class FeedBuzzSerializer(BuzzDetailSerializer):
    pass


class FeedRebuzzSerializer(RebuzzDetailSerializer):
    pass
