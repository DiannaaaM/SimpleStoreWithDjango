from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Create "Модератор продуктов" group with required permissions'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        content_type = ContentType.objects.get_for_model(Product)

        can_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Can unpublish product',
            content_type=content_type,
        )
        delete_perm = Permission.objects.get(codename='delete_product', content_type=content_type)

        group.permissions.add(can_unpublish, delete_perm)
        self.stdout.write(self.style.SUCCESS('Group "Модератор продуктов" is ready.'))
