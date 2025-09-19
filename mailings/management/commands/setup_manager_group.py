from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create Managers group with view permissions and disabling mailings'

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name='Менеджеры')
        perm_c = Permission.objects.filter(codename__in=[
            'can_view_all_clients', 'can_view_all_messages', 'can_view_all_mailings', 'can_disable_mailings'
        ])
        group.permissions.set(list(perm_c))
        self.stdout.write(self.style.SUCCESS('Managers group ensured'))


