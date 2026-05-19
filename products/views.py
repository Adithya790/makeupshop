

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from cart.models import Cart


def product_list(request):
    products = Product.objects.filter(stock__gt=0)

    categories = Category.objects.filter(parent=None)  # FIX HERE

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {
        'product': product
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, stock__gt=0)
    categories = Category.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products,
        'selected_category': category,
        'categories': categories
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect('cart_detail')