from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import UserLoginForm, RegisterForm
from .models import Sektant, Sekta, Nickname

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
            if user is not None:
                auth.login(request, user)
                return redirect('/my_sekts')
    else:
        form = UserLoginForm()

    context['form'] = form
    return render(request, 'login.html', context)

@login_required
def list_sekts_created_by_user(request):
    user_sekts = Sekta.objects.filter(creator=request.user)
    context = {'sekts':user_sekts}
    return render(request,'user_sekts_list.html',context)