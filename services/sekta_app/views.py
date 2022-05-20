from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import UserLoginForm, RegisterForm, SektaCreationForm
from .models import Sektant, Sekta, Nickname
from .helpers import is_belong


def home(request):
    return render(request, 'home.html', {})

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
def list_user_sekts(request):
    user_sekts = Sekta.objects.filter(creator=request.user)
    member_sekts = [nickname.sekta for nickname in Nickname.objects.filter(sektant=request.user)]
    context = {'user_sekts':user_sekts,'member_sekts':member_sekts}
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
    sekta = Sekta.objects.get(pk=id)
    participants = Nickname.objects.filter(sekta=sekta)
    if request.user != sekta.creator and not is_belong(sekta,request.user):
        return HttpResponse(status=403, content='Вы не входите в секту')
    context={'sekta':sekta,'participants':participants}
    if request.user==sekta.creator:
        context['creator']=True
    else:
        context['creator']=False
    return render(request,'sekta.html',context)

#todo: добавить уязвимость к parameter pollution
#todo: шифрование для никнейма
@login_required
def invite_sektant(request):
    follower = Sektant.objects.get(pk=int(request.GET.get('user')))
    sekta = Sekta.objects.get(pk=int(request.GET.get('sect')))
    new_name = request.GET.get('nickname')
    if request.user != sekta.creator:
        return HttpResponse(status=403, content='Вы не можете приглашать в чужую секту')
    if len(Nickname.objects.filter(sektant=follower).filter(sekta=sekta))>0:
        return HttpResponse(status=400, content='Этот пользователь уже в вашей секте')
    nickname = Nickname(sektant=follower,sekta=sekta,nickname=new_name)
    nickname.save()
    return HttpResponse(status=201, content='Сектант был успешно приглашён')

#form doesn't work. Only nickname parameter passes to form action, user.id and sect.id are missed + needed absolute path instead relative
@login_required
def invite_to_sekta(request,id):
    sekta = Sekta.objects.get(pk=id)
    if request.user != sekta.creator:
        return HttpResponse(status=403, content='Вы не можете приглашать в чужую секту')
    users = [user for user in Sektant.objects.filter(can_be_invited=True) if not is_belong(sekta,user) and user != sekta.creator]
    sekta = Sekta.objects.get(pk=id)
    context = {'sekta':sekta,'users':users}
    return render(request, 'invitation.html', context)

