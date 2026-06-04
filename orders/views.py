from django.shortcuts import render, redirect
from cart.models import Cart
from django.conf import settings
import razorpay
from .models import Order
from django.contrib.auth.decorators import login_required
@login_required
def checkout(request):

    cart_items = Cart.objects.all()

    total = sum(item.subtotal() for item in cart_items)

    if request.method == "POST":
        return redirect('payment')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def payment(request):

    amount = 50000  # ₹500 in paise

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order_id": order["id"],
        "amount": amount,
    }

    return render(request, "payment.html", context)

@login_required
def payment_success(request):

    payment_id = request.GET.get('payment_id')

    cart_items = Cart.objects.all()

    total = sum(item.subtotal() for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total=total,
        payment_id=payment_id,
        status='Confirmed'
    )

    cart_items.delete()

    return render(
        request,
        'payment_success.html',
        {'order': order}
    )

@login_required
def cod(request):

    cart_items = Cart.objects.all()

    total = sum(item.subtotal() for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total=total,
        payment_id="COD",
        status="Confirmed"
    )

    cart_items.delete()

    return render(
        request,
        'cod_success.html',
        {'order': order}
    )
@login_required
def track_order(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'track_order.html',
        {
            'order': order
        }
    )