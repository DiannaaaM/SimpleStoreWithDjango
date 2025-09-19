from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings

from catalog.models import Product, Category
try:
    from mailings.models import Mailing, Client, MailingAttempt
except Exception:  # pragma: no cover
    Mailing = None
    Client = None
    MailingAttempt = None


# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context)


def contacts(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'contacts.html', context)


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        if getattr(settings, 'CACHE_ENABLED', False):
            cache_key = 'product_list_queryset'
            products = cache.get(cache_key)
            if products is None:
                products = list(super().get_queryset())
                cache.set(cache_key, products, timeout=300)
            return products
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Mailing and Client:
            cache_key = 'homepage_mailing_stats'
            stats = None
            if getattr(settings, 'CACHE_ENABLED', False):
                stats = cache.get(cache_key)
            if stats is None:
                total_mailings = Mailing.objects.count()
                active_mailings = Mailing.objects.filter(status=Mailing.STATUS_RUNNING).count()
                unique_clients = Client.objects.count()
                stats = {
                    'total_mailings': total_mailings,
                    'active_mailings': active_mailings,
                    'unique_clients': unique_clients,
                }
                if getattr(settings, 'CACHE_ENABLED', False):
                    cache.set(cache_key, stats, timeout=300)
            context.update(stats)
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ("name", "description", "image", "category", "price")
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner_id == self.request.user.id


class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Product
    fields = ("name", "description", "image", "category", "price")
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner_id == request.user.id or request.user.has_perm('catalog.delete_product'):
            return super().dispatch(request, *args, **kwargs)
        return redirect('catalog:product_detail', pk=obj.pk)


class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.user.has_perm('catalog.can_unpublish_product'):
            product.is_published = False
            product.save(update_fields=['is_published'])
        return redirect('catalog:product_detail', pk=product.pk)


class ProductsByCategoryView(ListView):
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return context
