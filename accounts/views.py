from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):

    if request.method == 'POST':

        login_input = request.POST.get('login_input')
        password = request.POST.get('password')

        user = None

        # LOGIN WITH USERNAME

        if User.objects.filter(username=login_input).exists():

            username = User.objects.get(
                username=login_input
            ).username

            user = authenticate(
                request,
                username=username,
                password=password
            )

        # LOGIN WITH EMAIL

        elif User.objects.filter(email=login_input).exists():

            username = User.objects.get(
                email=login_input
            ).username

            user = authenticate(
                request,
                username=username,
                password=password
            )

        # LOGIN SUCCESS

        if user is not None:

            login(request, user)

            return redirect('/')

        else:

            messages.error(
                request,
                "Invalid login credentials"
            )

    return render(request, 'login.html')


def logout_view(request):

    logout(request)

    return redirect('/')


def create_account_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # PASSWORD CHECK

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match"
            )

            return redirect('create_account')

        # USERNAME EXISTS

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists"
            )

            return redirect('create_account')

        # EMAIL EXISTS

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already exists"
            )

            return redirect('create_account')

        # CREATE USER

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(
            request,
            "Account created successfully"
        )

        return redirect('login')

    return render(
        request,
        'create_account.html'
    )