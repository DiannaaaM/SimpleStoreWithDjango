from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from .forms import ClientForm, MessageForm, MailingForm
from .models import Client, Message, Mailing, MailingAttempt


class OwnerQuerySetMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.has_perm('mailings.can_view_all_mailings') or user.has_perm('mailings.can_view_all_clients') or user.has_perm('mailings.can_view_all_messages'):
            return qs
        return qs.filter(owner=user)


# Clients
class ClientListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, OwnerQuerySetMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner_id == self.request.user.id


class ClientUpdateView(LoginRequiredMixin, ClientOwnerRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, ClientOwnerRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


# Messages
class MessageListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, OwnerQuerySetMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner_id == self.request.user.id


class MessageUpdateView(LoginRequiredMixin, MessageOwnerRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(LoginRequiredMixin, MessageOwnerRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


# Mailings
class MailingListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Mailing


class MailingDetailView(LoginRequiredMixin, OwnerQuerySetMixin, DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner_id == self.request.user.id


class MailingUpdateView(LoginRequiredMixin, MailingOwnerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(LoginRequiredMixin, MailingOwnerRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')


class MailingSendView(LoginRequiredMixin, MailingOwnerRequiredMixin, View):
    def post(self, request, pk):
        mailing = Mailing.objects.select_related('message', 'owner').prefetch_related('clients').get(pk=pk)
        now = timezone.now()
        if mailing.finish_at and mailing.finish_at < now:
            mailing.status = Mailing.STATUS_FINISHED
            mailing.save(update_fields=["status"])
            return redirect('mailings:mailing_detail', pk=pk)

        if mailing.status == Mailing.STATUS_CREATED:
            mailing.status = Mailing.STATUS_RUNNING
            mailing.save(update_fields=["status"])

        for client in mailing.clients.all():
            try:
                sent = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=None,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status=MailingAttempt.STATUS_SUCCESS if sent else MailingAttempt.STATUS_FAIL,
                    server_response='OK' if sent else 'Unknown error',
                )
            except BadHeaderError as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status=MailingAttempt.STATUS_FAIL,
                    server_response=str(e),
                )
            except Exception as e:  # noqa
                MailingAttempt.objects.create(
                    mailing=mailing,
                    client=client,
                    status=MailingAttempt.STATUS_FAIL,
                    server_response=str(e),
                )

        if mailing.finish_at and mailing.finish_at < timezone.now():
            mailing.status = Mailing.STATUS_FINISHED
            mailing.save(update_fields=["status"])

        return redirect('mailings:mailing_detail', pk=pk)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('mailings.can_view_all_mailings'):
            return MailingAttempt.objects.select_related('mailing', 'client').order_by('-attempted_at')
        return MailingAttempt.objects.select_related('mailing', 'client').filter(mailing__owner=user).order_by('-attempted_at')


class MailingDisableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'mailings.can_disable_mailings'

    def post(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        mailing.status = Mailing.STATUS_FINISHED
        mailing.save(update_fields=["status"])
        return redirect('mailings:mailing_detail', pk=pk)


