from django.db import models

from bumblebee.buzzes.models import Buzz, Rebuzz
from bumblebee.comments.models import Comment
from bumblebee.notifications.choices import ACTION_TYPE, CONTENT_TYPE
from bumblebee.users.models import CustomUser


class BaseNotification(models.Model):
    """ """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    hide = models.BooleanField(default=False)

    class Meta:
        abstract = True


class NotificationMethods(models.Model):

    ##################################
    #           USERNAMES
    ##################################

    def get_usernames_from_user_ids(self, id_list: list) -> list:
        """
        Get list of usernames from ids of CustomUsers provided
        """

        user_instances = CustomUser.objects.filter(id__in=id_list).all()
        return [user.username for user in user_instances]

    def get_author_usernames_from_rebuzz_ids(self, id_list: list) -> list:
        """
        Get list of usernames of authors from ids of Rebuzz provided
        """
        rebuzz_instances = Rebuzz.objects.filter(id__in=id_list).all()
        return [rebuzz.author.username for rebuzz in rebuzz_instances]

    def get_commenter_usernames_from_comment_ids(self, id_list: list) -> list:
        """
        Get list of usernames of commenter from ids of comment provided
        """

        comment_instances = Rebuzz.objects.filter(id__in=id_list).all()
        return [comment.commenter.username for comment in comment_instances]

    ##################################
    #           STRING
    ##################################

    def get_notification(self, action, contenttype):
        """
        Generate string based on action and contenttype

        Eg, If a user commented on a rebuzz, it generates based on number of action doers
            a string like:
                `User1, User2 and # others commented on your rebuzz`
        """

        # CONTENT
        if contenttype == CONTENT_TYPE["BUZZ"]:
            interaction = self.buzz.buzz_interaction
        elif contenttype == CONTENT_TYPE["RBZ"]:
            interaction = self.rebuzz.rebuzz_interaction
        elif contenttype == CONTENT_TYPE["CMNT"]:
            interaction = self.comment.comment_interaction

        # ACTION
        if action == ACTION_TYPE["UPV"]:
            ids = interaction.upvotes
        elif action == ACTION_TYPE["DWV"]:
            ids = interaction.downvotes
        elif action == ACTION_TYPE["CMNT"]:
            ids = interaction.comments
        elif action == ACTION_TYPE["RBZ"]:
            ids = interaction.rebuzzes
        elif action == ACTION_TYPE["RPLY"]:
            ids = interaction.replies

        count = len(ids)
        usernames = self.get_usernames_from_user_ids(ids[-2:])
        username_count = len(usernames)
        if username_count != count:
            return f"{count} users have {action} your {contenttype}."

        else:
            if count == 1:
                return f"{usernames[-1]} {action} your {contenttype}."
            elif count == 2:
                return (
                    f"{usernames[-1]} and {usernames[-2]} {action} your {contenttype}."
                )
            elif count >= 2:
                return f"{usernames[-1]}, {usernames[-2]}, and {count-2} others {action} your {contenttype}."
            else:
                return f"0 users have {action} your {contenttype}."


#########################################
#           BUZZ
#########################################


class BuzzNotification(BaseNotification, NotificationMethods):
    """ """

    buzz = models.OneToOneField(
        Buzz, related_name="buzz_notification", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Buzz Notification"

    def __str__(self):
        return f"Buzz Notification- id:{self.buzz.id}"

    def get_upvote_notification(self):
        return self.get_notification(ACTION_TYPE["UPV"], CONTENT_TYPE["BUZZ"])

    def get_downvote_notification(self):
        return self.get_notification(ACTION_TYPE["DWV"], CONTENT_TYPE["BUZZ"])

    def get_rebuzz_notification(self):
        return self.get_notification(ACTION_TYPE["RBZ"], CONTENT_TYPE["BUZZ"])

    def get_comment_notification(self):
        return self.get_notification(ACTION_TYPE["CMNT"], CONTENT_TYPE["BUZZ"])


#########################################
#           REBUZZ
#########################################


class RebuzzNotification(BaseNotification, NotificationMethods):
    """ """

    rebuzz = models.OneToOneField(
        Rebuzz, related_name="rebuzz_notification", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Rebuzz Notification"

    def __str__(self):
        return f"Rebuzz Notification- id:{self.buzz.id}"

    def get_upvote_notification(self):
        return self.get_notification(ACTION_TYPE["UPV"], CONTENT_TYPE["RBZ"])

    def get_downvote_notification(self):
        return self.get_notification(ACTION_TYPE["DWV"], CONTENT_TYPE["RBZ"])

    def get_comment_notification(self):
        return self.get_notification(ACTION_TYPE["CMNT"], CONTENT_TYPE["RBZ"])


#########################################
#           COMMENTS
#########################################


class CommentNotification(BaseNotification, NotificationMethods):
    """ """

    comment = models.OneToOneField(
        Comment, related_name="comment_notification", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Rebuzz Notification"

    def __str__(self):
        return f"Rebuzz Notification- id:{self.buzz.id}"

    def get_upvote_notification(self):
        return self.get_notification(ACTION_TYPE["UPV"], CONTENT_TYPE["CMNT"])

    def get_downvote_notification(self):
        return self.get_notification(ACTION_TYPE["DWV"], CONTENT_TYPE["CMNT"])

    def get_reply_notification(self):
        return self.get_notification(ACTION_TYPE["RPLY"], CONTENT_TYPE["CMNT"])
