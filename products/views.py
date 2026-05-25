

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, CategoryBanner
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

    # selected category OR subcategory
    category = get_object_or_404(
        Category,
        slug=slug
    )

    # navbar categories
    categories = Category.objects.filter(parent=None)

    # subcategories
    subcategories = category.subcategories.all()

    # IF MAIN CATEGORY
    if subcategories.exists():

        products = Product.objects.filter(
            category__in=subcategories,
            stock__gt=0
        )

        # banners for main category
        banners = CategoryBanner.objects.filter(
            category=category
        )

    # IF SUBCATEGORY
    else:

        products = Product.objects.filter(
            category=category,
            stock__gt=0
        )

        # use parent category banners
        banners = CategoryBanner.objects.filter(
            category=category.parent
        )

    return render(request, 'products/product_list.html', {
        'products': products,
        'selected_category': category,
        'categories': categories,
        'subcategories': subcategories,
        'banners': banners,
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect('cart_detail')