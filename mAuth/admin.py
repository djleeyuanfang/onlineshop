from django.contrib import admin
from .models import *


@admin.register(User)
class MailCodeAdmin(admin.ModelAdmin):
    list_display = ("mail", "phone", "is_active", "is_admin", "last_login", "create_time")


@admin.register(MailCode)
class MailCodeAdmin(admin.ModelAdmin):
    list_display = ("mail", "code", "create_time")