from django.contrib import admin

# Register your models here.
from .models import Blocked, Follower, Following, Muted

admin.site.register(Following)
admin.site.register(Follower)
admin.site.register(Muted)
admin.site.register(Blocked)
