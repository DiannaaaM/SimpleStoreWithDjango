from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "owner")
    search_fields = ("email", "full_name")
    list_filter = ("owner",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "owner")
    search_fields = ("subject",)
    list_filter = ("owner",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "start_at", "finish_at", "owner")
    list_filter = ("status", "owner")
    filter_horizontal = ("clients",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "mailing", "client", "status", "attempted_at")
    list_filter = ("status", "attempted_at")


