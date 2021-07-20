from django.db import models
from django.contrib.postgres.fields import ArrayField


from bumblebee.users.models import CustomUser


class FeedMeta(models.Model):
    """ " """

    user = models.OneToOneField(
        CustomUser, related_name="user_feed_meta", on_delete=models.CASCADE
    )
    # feed_source_id = ArrayField(models.PositiveIntegerField(), blank=True, default=list)
    # blacklist_id = ArrayField(models.PositiveIntegerField(), blank=True, default=list)

    class Meta:
        verbose_name_plural = "FeedMeta"

    # def _generate_feed_source_id(self):
    #     """Generate feed source user ids by taking their folowing and removing blocked and muted"""

    #     following_ids = self.user.user_following.following
    #     muted_blocked_ids = self.user.user_muted.muted + self.user.user_blocked.blocked

    #     self.feed_source_id = list(set(following_ids) - set(muted_blocked_ids))
