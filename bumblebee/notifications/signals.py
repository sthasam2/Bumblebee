from django.dispatch import Signal, receiver

from bumblebee.notifications.utils import (
    create_new_follower_notification,
    create_new_follower_request_notification,
    create_new_follower_request_accept_notification,
    create_new_follower_request_reject_notification,
)

#  new follower signal instance
new_follower_signal = Signal(providing_args=["owner", "follower"])

#  new follower request signal instance
new_follower_request_signal = Signal(providing_args=["owner", "follower"])

#  new follower request accepted signal instance
new_follower_request_accept_signal = Signal(providing_args=["owner", "follower"])

#  new follower request rejected signal instance
new_follower_request_reject_signal = Signal(providing_args=["owner", "follower"])


@receiver(new_follower_signal)
def create_notification_on_follow(**kwargs):
    """ """

    print("Signal @create_notification_on_follow")

    create_new_follower_notification(
        owner=kwargs.get("owner"), follower=kwargs.get("follower")
    )


@receiver(new_follower_request_signal)
def create_notification_on_follow_request(**kwargs):
    """ """

    print("Signal @create_notification_on_follow_request")

    create_new_follower_request_notification(
        owner=kwargs.get("owner"), follow_requester=kwargs.get("follow_requester")
    )


@receiver(new_follower_request_accept_signal)
def create_notification_on_follow_request_accept(**kwargs):
    """ """

    print("Signal @create_notification_on_follow_request_accept")

    create_new_follower_request_accept_notification(
        owner=kwargs.get("owner"), follow_requester=kwargs.get("follow_requester")
    )


@receiver(new_follower_request_reject_signal)
def create_notification_on_follow_request_reject(**kwargs):
    """ """

    print("Signal @create_notification_on_follow_request_accept")

    create_new_follower_request_reject_notification(
        owner=kwargs.get("owner"), follow_requester=kwargs.get("follow_requester")
    )
