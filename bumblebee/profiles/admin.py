from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """"""

    list_display = ("user", "nickname", "phone", "location")
    list_filter = ("user",)
    search_fields = ("user", "nickname", "phone")
    ordering = ("-created_date",)
    # list_display = ("user", "action", "target", "created_date")
    # list_filter = "created_date"
    # search_fields = ("user", "action", "target")
    # ordering = ("-created_date",)


admin.site.register(Profile)