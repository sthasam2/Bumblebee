from django.contrib import admin

from .forms import BuzzAdminCreationForm, BuzzAdminForm
from .models import Buzz, BuzzImage, BuzzInteractions, Rebuzz


class BuzzAdmin(admin.ModelAdmin):
    """ """

    form = BuzzAdminForm
    add_form = BuzzAdminCreationForm

    list_display = ("id", "author", "content", "created_date")


admin.site.register(Buzz, BuzzAdmin)
admin.site.register(BuzzInteractions)
admin.site.register(BuzzImage)
admin.site.register(Rebuzz)
