from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('cod/', views.cod, name='cod'),
    path('track-order/<int:order_id>/',views.track_order,name='track_order'),
]