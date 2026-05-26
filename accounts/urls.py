from django.urls import path
from .views import *

urlpatterns = [

    path(
        'create-account/',
        create_account_view,
        name='create_account'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

]