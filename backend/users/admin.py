from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User

admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
