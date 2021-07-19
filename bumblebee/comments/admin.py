from django.contrib import admin

from .models import Comment, CommentInteractions

admin.site.register(Comment)
admin.site.register(CommentInteractions)
