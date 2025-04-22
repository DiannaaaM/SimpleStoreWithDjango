from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Category


# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context)

def contacts(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'contacts.html', context)


def products_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {"product": product})
