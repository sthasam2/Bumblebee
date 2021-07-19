from django.contrib.postgres.fields import ArrayField
from django.db import models

from bumblebee.users.models import CustomUser
from bumblebee.buzzes.models import Buzz


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
        null=False,
        related_name="buzz_comment",
        blank=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

    parent_rebuzz = models.ForeignKey(
        Buzz,
        null=True,
        related_name="rebuzz_comment",
        blank=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

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

    def __str__(self):
        return dict(
            comment=self.comment,
            upvotes=len(self.upvotes),
            downvotes=len(self.downvotes),
            replies=len(self.replies),
        ).__str__()
