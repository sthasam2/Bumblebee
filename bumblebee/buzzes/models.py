import uuid


from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse


from bumblebee.users.models import CustomUser


class Image(models.Model):
    """"""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
    image = models.ImageField(upload_to="media/")


class Buzz(models.Model):
    """"""

    class PrivacyChoices(models.TextChoices):
        """
        Choices for privacy options
        """

        PRIVATE = "priv", "private"  # only for self
        PUBLIC = "pub", "public"  # open for anyone public
        PROTECTED = "prot", "protected"  # only for followers

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
    user = models.ForeignKey(CustomUser, related_name="buzz", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    privacy = models.CharField(choices=PrivacyChoices.choices)

    # self
    content = models.CharField(
        max_length=1000, help_text="Something in your mind? Post a buzz", blank=True
    )
    images = models.ManyToManyField(
        Image, related_name="buzz_images", blank=True, none=True
    )
    location = models.CharField(max_length=500, blank=True, null=True)
    flair = ArrayField(models.CharField(max_length=100), blank=True)

    class Meta:
        verbose_name = "Buzz"
        verbose_name_plural = "Buzzes"
        ordering = ["-created_date"]

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("buzz-detail", kwargs={"uuid": self.uuid})


class Comment(models.Model):
    """"""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
    user = models.ForeignKey(CustomUser, related_name="buzz", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    content = models.TextField(max_length=1000, blank=False, null=False)
    images = models.ManyToManyField(
        Image, related_name="buzz_images", blank=True, none=True
    )
    flair = ArrayField(models.CharField(max_length=100), blank=True)

    def __str__(self):
        return self.content


class Interactions(models.Model):
    """"""

    buzz = models.ForeignKey(
        Buzz,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        unique=True,
    )
    views = models.IntegerField(blank=False, unique=False, default=0)
    upvotes = models.ManyToManyField(
        CustomUser, related_name="buzz_upvotes", blank=True
    )
    downvotes = models.ManyToManyField(
        CustomUser, related_name="buzz_downvotes", blank=True
    )
    comments = models.ManyToManyField(
        Comment, related_name="buzz_comments", blank=True, none=True
    )

    def __str__(self):
        return f'"buzz": {self.buzz},"views": {self.views},"upvotes": {self.upvotes.count()},"downvotes": {self.downvotes.count()}, "comments":{self.comments.count()}'


class CommentInteractions(Interactions):
    """"""

    comment = models.ForeignKey(Comment, blank=False, null=False)


class Rebuzz(Buzz):
    """"""

    buzz = models.ForeignKey(Buzz, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("rebuzz-detail", kwargs={"uuid": self.uuid})