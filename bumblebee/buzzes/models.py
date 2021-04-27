from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse

from bumblebee.comments.models import Comment
from bumblebee.users.models import CustomUser


class Buzz(models.Model):
    """
    A post for Content
    """

    class PrivacyChoices(models.TextChoices):
        """
        Choices for privacy options
        """

        PRIVATE = "priv", "private"  # only for self
        PUBLIC = "pub", "public"  # open for anyone public
        PROTECTED = "prot", "protected"  # only for followers

    author = models.ForeignKey(
        CustomUser, related_name="buzz_author", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    privacy = models.CharField(max_length=25, choices=PrivacyChoices.choices)

    # self
    content = models.CharField(
        max_length=1000, help_text="Something in your mind? Post a buzz", blank=True
    )
    image = models.ImageField(upload_to="media/buzzes/image")
    location = models.CharField(max_length=500, blank=True, null=True)
    flair = ArrayField(models.CharField(max_length=100), blank=True)

    class Meta:
        """"""

        verbose_name = "Buzz"
        verbose_name_plural = "Buzzes"
        ordering = ["-created_date"]

    def __str__(self):
        """"""
        return self.content

    def get_absolute_url(self):
        """"""
        return reverse("buzz-detail", kwargs={"id": self.id})


class BuzzInteractions(models.Model):
    """"""

    buzz = models.OneToOneField(
        Buzz,
        related_name="owner_buzz",
        on_delete=models.CASCADE,
    )
    views = models.IntegerField(blank=False, unique=False, default=0)
    upvotes = models.ManyToManyField(
        CustomUser, related_name="buzz_upvotes", blank=True
    )
    downvotes = models.ManyToManyField(
        CustomUser, related_name="buzz_downvotes", blank=True
    )
    comments = models.ManyToManyField(Comment, related_name="buzz_comments", blank=True)

    def __str__(self):
        return f'"buzz": {self.buzz},"views": {self.views},"upvotes": {self.upvotes.count()},"downvotes": {self.downvotes.count()}, "comments":{self.comments.count()}'


class Rebuzz(Buzz):
    """
    Rebuzz post of a buzz
    """

    # for clash issues on inheritence, explicitly defining the inherited model
    _inherited_from = models.OneToOneField(
        Buzz,
        parent_link=True,
        related_name="Inherited_from",
        on_delete=models.CASCADE,
    )

    # referenced rebuzz
    rebuzz_of = models.ForeignKey(
        Buzz,
        related_name="rebuzz_of+",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Rebuzz"
        verbose_name_plural = "Rebuzzes"

    def get_absolute_url(self):
        return reverse("rebuzz-detail", kwargs={"id": self.id})