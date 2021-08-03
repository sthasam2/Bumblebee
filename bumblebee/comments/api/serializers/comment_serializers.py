"""
Serializers for Comments
"""

from rest_framework import serializers

from bumblebee.comments.models import Comment
from bumblebee.core.exceptions import UnknownModelFieldsError

from .commenter_serializers import CommentUserSerializer
from .interaction_serializers import CommentInteractionsSerializer

######################################
##           RETRIEVE
######################################


class CommentDetailSerializer(serializers.ModelSerializer):
    """ """

    commentid = serializers.IntegerField(source="id")

    created_date = serializers.DateTimeField()
    edited_date = serializers.DateTimeField()
    edited = serializers.BooleanField()

    content = serializers.CharField(help_text="Something in your mind? Post a buzz")
    flair = serializers.ListField(child=serializers.CharField())

    commenter = CommentUserSerializer(many=False)
    image = serializers.ImageField()
    interaction = CommentInteractionsSerializer(
        source="comment_interaction", read_only=True
    )

    level = serializers.IntegerField()
    parent_buzz = serializers.PrimaryKeyRelatedField(read_only=True)
    parent_rebuzz = serializers.PrimaryKeyRelatedField(read_only=True)
    parent_comment = serializers.PrimaryKeyRelatedField(read_only=True)

    sentiment_value = serializers.FloatField() 
    textblob_value = serializers.FloatField()


    class Meta:
        model = Comment
        fields = [
            "commentid",
            "created_date",
            "edited_date",
            "edited",
            "level",
            "content",
            "flair",
            "commenter",
            "image",
            "interaction",
            "parent_buzz",
            "parent_rebuzz",
            "parent_comment",
            "sentiment_value",
            "textblob_value",
        ]


######################################
##           CREATE
######################################


class CreateCommentSerializer(serializers.ModelSerializer):
    """ """

    content = serializers.CharField(
        required=False, help_text="Something in your mind? Post a buzz"
    )
    image = serializers.ImageField(
        required=False, help_text="Need a Visual feedback? Add an image"
    )
    flair = serializers.ListField(child=serializers.CharField(), required=False)
    level = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = [
            "content",
            "image",
            "flair",
            "level",
        ]


######################################
##           UPDATE
######################################


class EditCommentSerializer(serializers.ModelSerializer):
    """ """

    content = serializers.CharField(
        required=False, help_text="Something in your mind? Post a buzz"
    )
    flair = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Comment
        fields = ["content", "flair"]

    def update_comment(self, comment_instance, **validated_data):
        """ """
        try:
            for key, value in validated_data.items():
                if comment_instance.__dict__.__contains__(key):
                    if comment_instance.__getattribute__(key) != value:
                        comment_instance.__setattr__(key, value)
                else:
                    raise UnknownModelFieldsError(
                        key,
                        f"'{comment_instance.__class__.__name__}' object has no model field called {key}",
                    )
            if comment_instance.__getattribute__("edited") != True:
                comment_instance.__setattr__("edited", True)

            comment_instance.save()

        except UnknownModelFieldsError as error:
            print(error)
            raise error

        except Exception as error:
            print("ERROR @update_comment\n", error)
            raise error
