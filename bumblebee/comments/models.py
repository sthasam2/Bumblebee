from django.contrib.postgres.fields import ArrayField
from django.db import models

from bumblebee.buzzes.models import Buzz, Rebuzz
from bumblebee.users.models import CustomUser


class IdDateField(models.Model):
    """ """

    userid = models.PositiveIntegerField()
    date = models.DateTimeField()


class AbstractComment(models.Model):
    """ """

    commenter = models.ForeignKey(
        CustomUser, related_name="comment_user", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    content = models.TextField(max_length=1000, blank=False, null=False)
    image = models.ImageField(upload_to="comments/image", blank=True, null=True)

    flair = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    parent_buzz = models.ForeignKey(
        Buzz,
        related_name="buzz_comment",
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

    parent_rebuzz = models.ForeignKey(
        Rebuzz,
        related_name="rebuzz_comment",
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

    sentiment_value = models.FloatField(null=True, blank=True)
    textblob_value = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.content


class Comment(AbstractComment):
    """ """

    level = models.PositiveIntegerField(blank=False, default=1)
    parent_comment = models.PositiveIntegerField(
        null=True, blank=True, db_index=True, default=None
    )

    def __str__(self):
        return self.content


class CommentInteractions(models.Model):
    """ """

    comment = models.OneToOneField(
        Comment,
        related_name="comment_interaction",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    upvotes = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )
    downvotes = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )
    replies = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )
    updated_date = models.DateTimeField(auto_now=True)

    def get_upvote_count(self):
        return len(self.upvotes)

    def get_downvote_count(self):
        return len(self.downvotes)

    def get_reply_count(self):
        return len(self.replies)

    def __str__(self):
        return dict(
            comment=self.comment,
            upvotes=self.get_upvote_count(),
            downvotes=self.get_downvote_count(),
            replies=self.get_reply_count(),
        ).__str__()


class CommentUpvoteDownvoteMeta(models.Model):
    """ """

    class ActionChoices(models.TextChoices):
        """
        Choices for action options
        """

        UPVOTE = "upv", "upvote"
        DOWNVOTE = "downvote", "downvote"  # open for anyone public

    comment_interaction = models.ForeignKey(
        CommentInteractions,
        related_name="comment_interaction_upvdwv_meta",
        on_delete=models.CASCADE,
    )
    action = models.CharField(max_length=100, choices=ActionChoices.choices)
    userid = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"userid: {self.userid} {self.action} Comment on {self.date}"
