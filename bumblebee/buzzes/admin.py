from django.contrib import admin

from .models import Buzz, Rebuzz, BuzzInteractions


admin.site.register(Buzz)
admin.site.register(Rebuzz)
admin.site.register(BuzzInteractions)
