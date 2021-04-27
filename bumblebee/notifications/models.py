# TODO add modeling

from django.db import models

# Create your models here.
class BaseNotification(models.Model):
    """"""

    class Meta:
        abstract = True

    pass


class PostNotification(BaseNotification):
    pass


class UserRelationNotification(BaseNotification):
    pass


class CommunityNotification(BaseNotification):
    pass
