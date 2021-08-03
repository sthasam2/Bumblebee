"""
Notification Utility Function
"""
from django.db.models import Q

from bumblebee.notifications.choices import ACTION_TYPE, CONTENT_TYPE
from bumblebee.notifications.models.grouped_models import (
    BuzzNotification,
    CommentNotification,
    RebuzzNotification,
)
from bumblebee.notifications.models.individual_models import (
    CommentBuzzNotification,
    CommentRebuzzNotification,
    DownvoteBuzzNotification,
    DownvoteCommentNotification,
    DownvoteRebuzzNotification,
    NewFollowerNotification,
    NewFollowerRequestNotification,
    AcceptedFollowerRequestNotification,
    RejectedFollowerRequestNotification,
    RebuzzBuzzNotification,
    ReplyCommentNotification,
    UpvoteBuzzNotification,
    UpvoteCommentNotification,
    UpvoteRebuzzNotification,
)

###########################################
#           CONNECTION CREATE
###########################################


def create_notification(action, contenttype, agent, instance, offshoot=None):
    """ """

    if contenttype == CONTENT_TYPE["BUZZ"]:
        if action == ACTION_TYPE["UPV"]:
            UpvoteBuzzNotification.objects.create(
                agent=agent, user=instance.author, buzz=instance
            )
        elif action == ACTION_TYPE["DWV"]:
            DownvoteBuzzNotification.objects.create(
                agent=agent, user=instance.author, buzz=instance
            )
        elif action == ACTION_TYPE["CMNT"]:
            CommentBuzzNotification.objects.create(
                agent=agent, user=instance.author, buzz=instance, comment=offshoot
            )
        elif action == ACTION_TYPE["RBZ"]:
            RebuzzBuzzNotification.objects.create(
                agent=agent, user=instance.author, buzz=instance, rebuzz=offshoot
            )

    elif contenttype == CONTENT_TYPE["RBZ"]:
        if action == ACTION_TYPE["UPV"]:
            UpvoteRebuzzNotification.objects.create(
                agent=agent, user=instance.author, rebuzz=instance
            )
        elif action == ACTION_TYPE["DWV"]:
            DownvoteRebuzzNotification.objects.create(
                agent=agent, user=instance.author, rebuzz=instance
            )
        elif action == ACTION_TYPE["CMNT"]:
            CommentRebuzzNotification.objects.create(
                agent=agent, user=instance.author, rebuzz=instance, comment=offshoot
            )

    elif contenttype == CONTENT_TYPE["CMNT"]:
        if instance.parent_buzz is not None:
            user = instance.parent_buzz.author
        elif instance.parent_rebuzz.author is not None:
            user = instance.parent_rebuzz.author

        if action == ACTION_TYPE["UPV"]:
            UpvoteCommentNotification.objects.create(
                agent=agent, user=user, comment=instance
            )
        elif action == ACTION_TYPE["DWV"]:
            DownvoteCommentNotification.objects.create(
                agent=agent, user=user, comment=instance
            )
        elif action == ACTION_TYPE["RPLY"]:
            ReplyCommentNotification.objects.create(
                agent=agent, user=user, comment=instance, reply=offshoot
            )


def delete_notification(action, contenttype, agent, instance):
    """ """

    if contenttype == CONTENT_TYPE["BUZZ"]:
        if action == ACTION_TYPE["UPV"]:
            UpvoteBuzzNotification.objects.filter(
                Q(agent=agent), Q(buzz=instance)
            ).delete()
        elif action == ACTION_TYPE["DWV"]:
            UpvoteBuzzNotification.objects.filter(
                Q(agent=agent), Q(buzz=instance)
            ).delete()
        elif action == ACTION_TYPE["CMNT"]:
            UpvoteBuzzNotification.objects.filter(
                Q(agent=agent), Q(buzz=instance)
            ).delete()
        elif action == ACTION_TYPE["RBZ"]:
            UpvoteBuzzNotification.objects.filter(
                Q(agent=agent), Q(buzz=instance)
            ).delete()
        elif action == ACTION_TYPE["RPLY"]:
            UpvoteBuzzNotification.objects.filter(
                Q(agent=agent), Q(buzz=instance)
            ).delete()

    elif contenttype == CONTENT_TYPE["RBZ"]:
        if action == ACTION_TYPE["UPV"]:
            UpvoteRebuzzNotification.objects.filter(
                Q(agent=agent), Q(rebuzz=instance)
            ).delete()
        elif action == ACTION_TYPE["DWV"]:
            DownvoteRebuzzNotification.objects.filter(
                Q(agent=agent), Q(rebuzz=instance)
            ).delete()
        elif action == ACTION_TYPE["CMNT"]:
            CommentRebuzzNotification.objects.filter(
                Q(agent=agent), Q(rebuzz=instance)
            ).delete()

    elif contenttype == CONTENT_TYPE["CMNT"]:
        if action == ACTION_TYPE["UPV"]:
            UpvoteCommentNotification.objects.filter(
                Q(agent=agent), Q(comment=instance)
            ).delete()
        elif action == ACTION_TYPE["DWV"]:
            DownvoteCommentNotification.objects.filter(
                Q(agent=agent), Q(comment=instance)
            ).delete()
        elif action == ACTION_TYPE["RPLY"]:
            ReplyCommentNotification.objects.filter(
                Q(agent=agent), Q(comment=instance)
            ).delete()


def create_new_follower_notification(owner, follower):
    """Create a new follower notification instance"""

    return NewFollowerNotification.objects.create(user=owner, follower=follower)


def create_new_follower_request_notification(owner, follow_requester):
    """Create a new follower request notification instance"""

    return NewFollowerRequestNotification.objects.create(user=owner, follow_requester=follow_requester)

def create_new_follower_request_accept_notification(owner, follow_requester):
    """Create a new follower request accept notification instance"""

    return AcceptedFollowerRequestNotification.objects.create(user=owner, follow_requester=follow_requester)

def create_new_follower_request_reject_notification(owner, follow_requester):
    """Create a new follower request reject notification instance"""

    return RejectedFollowerRequestNotification.objects.create(user=owner, follow_requester=follow_requester)


####################################################
#               RETRIEVE
####################################################


def get_notifications_for_userid(userid):
    """ """

    buzz_notification = BuzzNotification.objects.filter(user__id=userid).exclude(
        hide=True
    )
    rebuzz_notification = RebuzzNotification.objects.filter(user__id=userid).exclude(
        hide=True
    )
    comment_notification = CommentNotification.objects.filter(user__id=userid).exclude(
        hide=True
    )
    follower_notification = NewFollowerNotification.objects.filter(
        user__id=userid
    ).exclude(hide=True)
    follower_request_notification = NewFollowerRequestNotification.objects.filter(
        user__id=userid
    ).exclude(hide=True)

    return dict(
        buzz_notification=buzz_notification,
        rebuzz_notification=rebuzz_notification,
        comment_notification=comment_notification,
        follower_notification=follower_notification,
        follower_request_notification=follower_request_notification,
    )


def get_individual_notifications_for_userid(userid):
    """ """

    buzz_notification = dict(
        upvote_notification=UpvoteBuzzNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        downvote_notification=DownvoteBuzzNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        comment_notification=CommentBuzzNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        rebuzz_notification=RebuzzBuzzNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
    )

    rebuzz_notification = dict(
        upvote_notification=UpvoteRebuzzNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        downvote_notification=DownvoteRebuzzNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        comment_notification=CommentRebuzzNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
    )
    comment_notification = dict(
        upvote_notification=UpvoteCommentNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        downvote_notification=DownvoteCommentNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        reply_notification=ReplyCommentNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
    )

    connection_notification = dict(
        follower_notification=NewFollowerNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        follower_request_notification=NewFollowerRequestNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        follower_request_accept_notification=AcceptedFollowerRequestNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
        follower_request_reject_notification=RejectedFollowerRequestNotification.objects.filter(
            user__id=userid
        ).exclude(hide=True),
    )

    return dict(
        buzz_notification=buzz_notification,
        rebuzz_notification=rebuzz_notification,
        comment_notification=comment_notification,
        connection_notification=connection_notification,
    )
