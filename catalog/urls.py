from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('catalog/create', ProductCreateView.as_view(), name="products_create"),
    path('catalog/<int:pk>/update', ProductUpdateView.as_view(), name="products_update"),
    path('catalog/<int:pk>/delete', ProductDeleteView.as_view(), name="products_delete"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:pk>/edit/', product_update, name='product_edit'),
    path('products/<int:pk>/delete/', product_delete, name='product_delete'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
