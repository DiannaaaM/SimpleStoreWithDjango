from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError

from mailings.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = 'Send a mailing by id: python manage.py send_mailing <mailing_id>'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int)

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        try:
            mailing = Mailing.objects.select_related('message').prefetch_related('clients').get(pk=mailing_id)
        except Mailing.DoesNotExist:
            raise CommandError('Mailing not found')

        now = timezone.now()
        if mailing.finish_at and mailing.finish_at < now:
            self.stdout.write(self.style.WARNING('Mailing already finished'))
            mailing.status = Mailing.STATUS_FINISHED
            mailing.save(update_fields=["status"])
            return

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

        self.stdout.write(self.style.SUCCESS('Mailing processed'))


