from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "user"]
    list_display_links = ["id", "user", "author"]
    search_fields = ["user", "author"]


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscribeAdmin)
