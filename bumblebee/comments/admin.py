from django.contrib import admin

from .models import Comment, CommentInteractions, CommentUpvoteDownvoteMeta

admin.site.register(Comment)
admin.site.register(CommentInteractions)
admin.site.register(CommentUpvoteDownvoteMeta)
