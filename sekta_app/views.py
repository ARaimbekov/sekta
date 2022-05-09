from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import UserLoginForm, RegisterForm, SektaCreationForm
from .models import Sektant, Sekta, Nickname
from .helpers import is_belong

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

@login_required
def create_sekta(request):
    context={}
    if request.method == 'POST':
        form = SektaCreationForm(data=request.POST)
        if form.is_valid():
            sektaname=request.POST['sektaname']
            sekta = form.save(request.user)
            return redirect(f'/sekta/{sekta.id}')
        else:
            return HttpResponse(status=400,content='Секта с таким именем уже есть')
    else:
        form = SektaCreationForm()
        context['form'] = form
        return render(request,'create_sekta.html',context)

@login_required
def show_sekta(request,id):
    sekta = Sekta.objects.filter(id=id)[0]
    participants = Nickname.objects.filter(sekta=sekta)
    if request.user != sekta.creator and not is_belong(sekta,request.user):
        return HttpResponse(status=403, content='Вы не входите в секту')
    context={'sekta':sekta,'participants':participants}
    return render(request,'sekta.html',context)
