from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductUnpublishView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('catalog/create', ProductCreateView.as_view(), name="products_create"),
    path('catalog/<int:pk>/update', ProductUpdateView.as_view(), name="products_update"),
    path('catalog/<int:pk>/delete', ProductDeleteView.as_view(), name="products_delete"),
    path('catalog/<int:pk>/unpublish', ProductUnpublishView.as_view(), name='product_unpublish'),
]
