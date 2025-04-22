from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Add test product'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        Product.objects.create(name="test", description="test", price="100", created_at="2024-12-04", updated_at="2024-12-04")
