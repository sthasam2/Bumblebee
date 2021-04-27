from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from bumblebee.users.models import CustomUser


class Comment(models.Model):
    """"""

    author = models.ForeignKey(
        CustomUser, related_name="comment_author", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    content = models.TextField(max_length=1000, blank=False, null=False)
    image = models.ImageField(upload_to="media/comments/image")

    flair = ArrayField(models.CharField(max_length=100), blank=True)

    _parent_buzz = models.PositiveIntegerField(null=False, blank=True, db_index=True)
    _parent_comment = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    def __str__(self):
        return self.content


class CommentInteractions(models.Model):
    """"""

    comment = models.OneToOneField(
        Comment,
        related_name="owner_comment",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    upvotes = models.ManyToManyField(
        CustomUser, related_name="comment_upvotes", blank=True
    )
    downvotes = models.ManyToManyField(
        CustomUser, related_name="comment_downvotes", blank=True
    )
    comments = models.ManyToManyField(
        Comment, related_name="comment_replies", blank=True
    )

    def __str__(self):
        return f'"buzz": {self.buzz},"views": {self.views},"upvotes": {self.upvotes.count()},"downvotes": {self.downvotes.count()}, "comments":{self.comments.count()}'
