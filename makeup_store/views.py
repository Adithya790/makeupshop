from django.shortcuts import render

def home(request):
    return render(request,'base.html')

def cart(request):
    return render(request, 'cart/cart.html')