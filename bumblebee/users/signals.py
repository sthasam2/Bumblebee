from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType


from .models import CustomUser
from bumblebee.profiles.models import Profile
from bumblebee.activities.models import UserActivity, Activity


@receiver(post_save, sender=CustomUser)
def post_save_create_save_profile_and_activity(sender, instance, created, **kwargs):
    if created:
        print("signal received")
        # create profile
        Profile.objects.create(user=instance)
        #  create activity
        Activity.objects.create(
            action=UserActivity.Actions.SIGN_UP,
            target_content=ContentType.objects.get_for_model(CustomUser),
            target_id=instance.id,
        )
        # link activity and user
        UserActivity.objects.create(
            user=instance,
        )
