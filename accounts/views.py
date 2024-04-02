from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')  # Grab the email from the form
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                context = 'Username has already been taken!'
                return render(request, 'accounts/signup.html', {'error': context})
            elif User.objects.filter(email=email).exists():  # Check if the email already exists
                context = 'Email has already been registered!'
                return render(request, 'accounts/signup.html', {'error': context})
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                auth.login(request, user)
                return redirect('home')
        else:
            context = 'Passwords must match!'
            return render(request, 'accounts/signup.html', {'error': context})

    return render(request, 'accounts/signup.html')



def login(request):
    if request.method == 'POST':
        login = request.POST.get('username')  # 'login' can be either an email or a username
        password = request.POST.get('password')

        user = None

        # Check if 'login' is an email address
        if '@' in login:
            try:
                user = User.objects.get(email=login)  # Try to find user by email
                user = auth.authenticate(request, username=user.username, password=password)  # Authenticate using the username
            except User.DoesNotExist:
                user = None  # If no user found by email, keep user as None
        else:
            user = auth.authenticate(request, username=login, password=password)  # Direct authentication attempt

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context = 'Username, Email or Password is incorrect'
            return render(request, 'accounts/login.html', {'error': context})
            
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')
