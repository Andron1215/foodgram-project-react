from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "user"]
    list_display_links = ["id"]
    search_fields = ["id", "author", "user"]
    filter_horizontal = ["user"]
    filter_vertical = ["author"]


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscribeAdmin)
