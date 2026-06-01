

from django.shortcuts import render, redirect
from .models import Cart


def cart_detail(request):
    cart_items = Cart.objects.all()
    total = 0

    for item in cart_items:
        total += item.subtotal()

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
    })


def add_quantity(request, product_id):
    try:
        cart_item = Cart.objects.get(product__id=product_id)
        cart_item.quantity += 1
        cart_item.save()
    except Cart.DoesNotExist:
        pass

    return redirect('cart_detail')


def decrease_quantity(request, product_id):
    try:
        cart_item = Cart.objects.get(product__id=product_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except Cart.DoesNotExist:
        pass

    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    try:
        cart_item = Cart.objects.get(product__id=product_id)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart_detail')