from .models import UserActivity


def _create_activity(
    user: object, action: str, target_content: object = None, target_id: int = None
):
    """
    Creates activity based on certain actions by the user
    """

    activity = UserActivity(
        user=user, action=action, target_content=target_content, target_id=target_id
    )
    activity.save()


# FIXME add checks for previous activity, spammy behaviour etc