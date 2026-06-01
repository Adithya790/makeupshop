from django.shortcuts import render, redirect
from cart.models import Cart

def checkout(request):

    cart_items = Cart.objects.all()

    total = sum(item.subtotal() for item in cart_items)

    if request.method == "POST":
        return redirect('payment')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


def payment(request):
    return render(request, 'payment.html')
