from django.db import models

from bumblebee.buzzes.models import Buzz, Rebuzz
from bumblebee.comments.models import Comment
from bumblebee.notifications.choices import ACTION_TYPE, CONTENT_TYPE
from bumblebee.users.models import CustomUser


class BaseNotification(models.Model):
    """ """

    timestamp = models.DateTimeField(auto_now_add=True)
    hide = models.BooleanField(default=False)

    class Meta:
        abstract = True


#########################################
#           BUZZ
#########################################


class UpvoteBuzzNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_buzz_upvote_notification",
        on_delete=models.CASCADE,
    )
    buzz = models.ForeignKey(
        Buzz, related_name="buzz_upvote_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_upvoted_buzz_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Buzz Upvote Notification"

    def __str__(self):
        return f"{self.agent.username} upvoted your buzz"


class DownvoteBuzzNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_buzz_downvote_notification",
        on_delete=models.CASCADE,
    )
    buzz = models.ForeignKey(
        Buzz, related_name="buzz_downvote_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_downvoted_buzz_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Buzz Downvote Notification"

    def __str__(self):
        return f"{self.agent.username} downvoted your buzz"


class CommentBuzzNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_buzz_comment_notification",
        on_delete=models.CASCADE,
    )
    buzz = models.ForeignKey(
        Buzz, related_name="buzz_comment_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_commented_buzz_notification",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment,
        related_name="comment_buzz_comment_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Buzz Comment Notification"

    def __str__(self):
        return f"{self.agent.username} commented on your buzz"


class RebuzzBuzzNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_buzz_rebuzz_notification",
        on_delete=models.CASCADE,
    )
    buzz = models.ForeignKey(
        Buzz, related_name="buzz_rebuzz_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_rebuzzed_buzz_notification",
        on_delete=models.CASCADE,
    )
    rebuzz = models.ForeignKey(
        Rebuzz, related_name="rebuzz_buzz_rebuzz_notification", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Buzz Rebuzz Notification"

    def __str__(self):
        return f"{self.agent.username} rebuzzed your buzz"


#########################################
#           REBUZZ
#########################################


class UpvoteRebuzzNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_rebuzz_upvote_notification",
        on_delete=models.CASCADE,
    )
    rebuzz = models.ForeignKey(
        Rebuzz, related_name="rebuzz_upvote_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_upvoted_rebuzz_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Rebuzz Upvote Notification"

    def __str__(self):
        return f"{self.agent.username} upvoted your rebuzz"


class DownvoteRebuzzNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_rebuzz_downvote_notification",
        on_delete=models.CASCADE,
    )
    rebuzz = models.ForeignKey(
        Rebuzz, related_name="rebuzz_downvote_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_downvoted_rebuzz_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Rebuzz Downvote Notification"

    def __str__(self):
        return f"{self.agent.username} downvoted your rebuzz"


class CommentRebuzzNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_rebuzz_comment_notification",
        on_delete=models.CASCADE,
    )
    rebuzz = models.ForeignKey(
        Rebuzz, related_name="rebuzz_comment_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_commented_rebuzz_notification",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment,
        related_name="comment_rebuzz_comment_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Rebuzz Comment Notification"

    def __str__(self):
        return f"{self.agent.username} commented on your rebuzz"


#########################################
#           COMMENTS
#########################################


class UpvoteCommentNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_comment_upvote_notification",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment, related_name="comment_upvote_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_upvoted_comment_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Comment Upvote Notification"

    def __str__(self):
        return f"{self.agent.username} upvoted your comment"


class DownvoteCommentNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_comment_downvote_notification",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment, related_name="comment_downvote_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_downvoted_comment_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Comment Downvote Notification"

    def __str__(self):
        return f"{self.agent.username} downvoted your comment"


class ReplyCommentNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_comment_reply_notification",
        on_delete=models.CASCADE,
    )

    comment = models.ForeignKey(
        Comment, related_name="comment_reply_notification", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        CustomUser,
        related_name="user_replied_comment_notification",
        on_delete=models.CASCADE,
    )
    reply = models.ForeignKey(
        Comment,
        related_name="comment_reply_comment_notification",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Comment Reply Notification"

    def __str__(self):
        return f"{self.agent.username} replied on your your comment"


#########################################
#           CONNECTIONS
#########################################


class NewFollowerNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_new_follower_notification",
        on_delete=models.CASCADE,
    )

    follower = models.ForeignKey(
        CustomUser, related_name="notification_for_following", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "New Follower Notification"

    def __str__(self):
        return f"{self.follower.username} followed you"


class NewFollowerRequestNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_new_follower_request_notification",
        on_delete=models.CASCADE,
    )

    follow_requester = models.ForeignKey(
        CustomUser,
        related_name="notification_for_following_request",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "New Follower Request Notification"

    def __str__(self):
        return f"{self.follow_requester.username} requiested to followed you."


class AcceptedFollowerRequestNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_new_follower_request_accepted_notification",
        on_delete=models.CASCADE,
    )

    follow_requester = models.ForeignKey(
        CustomUser,
        related_name="notification_for_accepted_following_request",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Follower Accept Request Notification"

    def __str__(self):
        return (
            f"{self.follow_requester.username} accepted your request to followed them"
        )


class RejectedFollowerRequestNotification(BaseNotification):
    """ """

    user = models.ForeignKey(
        CustomUser,
        related_name="user_new_follower_request_rejected_notification",
        on_delete=models.CASCADE,
    )

    follow_requester = models.ForeignKey(
        CustomUser,
        related_name="notification_for_rejected_following_request",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Follower Reject Request Notification"

    def __str__(self):
        return f"{self.follow_requester.username} rejected your request to follow them"
