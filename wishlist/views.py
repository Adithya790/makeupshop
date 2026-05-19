from django.shortcuts import render, get_object_or_404, redirect
from .models import Wishlist
from products.models import Product


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(product=product)

    return redirect('wishlist_detail')


def wishlist_detail(request):
    wishlist_items = Wishlist.objects.all()

    return render(request, 'wishlist/wishlist_detail.html', {
        'wishlist_items': wishlist_items
    })


def remove_from_wishlist(request, product_id):
    try:
        wishlist_item = Wishlist.objects.get(product__id=product_id)
        wishlist_item.delete()
    except Wishlist.DoesNotExist:
        pass

    return redirect('wishlist_detail')
