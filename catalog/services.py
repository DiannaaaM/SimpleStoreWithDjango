from django.core.cache import cache
from django.conf import settings
from .models import Product


def get_products_by_category(category_id):
    cache_key = f"products_by_category:{category_id}"
    if getattr(settings, 'CACHE_ENABLED', False):
        products = cache.get(cache_key)
        if products is not None:
            return products
    products = Product.objects.filter(category_id=category_id)
    if getattr(settings, 'CACHE_ENABLED', False):
        cache.set(cache_key, list(products), timeout=300)
    return products
