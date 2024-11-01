# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Discount
from django.contrib.auth.models import User
from django.contrib import messages

def discount_list(request):
    discounts = Discount.objects.all()
    return render(request, 'discount_list.html', {'discounts': discounts})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('discount_list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Username already exists')
    return render(request, 'register.html')
