from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import UserLoginForm, RegisterForm
from .models import Sektant

def register(request):
    context={}
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()

    context['form'] = form
    return render(request, 'register.html', context)

def login(request):
    context={}
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
    else:
        form = UserLoginForm()

    context['form'] = form
    return render(request, 'login.html', context)