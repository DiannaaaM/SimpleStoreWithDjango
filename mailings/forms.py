from django import forms
from .models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("email", "full_name", "comment")


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "body")


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("start_at", "finish_at", "status", "message", "clients")


