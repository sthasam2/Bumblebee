from django.contrib import admin

# Register your models here.
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
    RebuzzBuzzNotification,
    ReplyCommentNotification,
    UpvoteBuzzNotification,
    UpvoteCommentNotification,
    UpvoteRebuzzNotification,
)

admin.site.register(BuzzNotification)
admin.site.register(RebuzzNotification)
admin.site.register(CommentNotification)
admin.site.register(NewFollowerNotification)
admin.site.register(NewFollowerRequestNotification)
admin.site.register(UpvoteBuzzNotification)
admin.site.register(DownvoteBuzzNotification)
admin.site.register(RebuzzBuzzNotification)
admin.site.register(CommentBuzzNotification)
admin.site.register(UpvoteRebuzzNotification)
admin.site.register(DownvoteRebuzzNotification)
admin.site.register(CommentRebuzzNotification)
admin.site.register(UpvoteCommentNotification)
admin.site.register(DownvoteCommentNotification)
admin.site.register(ReplyCommentNotification)
