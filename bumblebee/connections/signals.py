from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from bumblebee.activities.models import UserActivity
from bumblebee.activities.utils import _create_activity

# from .models import Foller, Following, Muted, Blocked


# @receiver(post_save, sender=Muted)
# def post_save_create_interaction_activity(sender, instance, created, **kwargs):
#     """ """

#     if created:
#         pass


# @receiver(post_save, sender=Blocked)
# def post_save_create_interaction_activity(sender, instance, created, **kwargs):
#     """ """

#     if created:
#         pass
