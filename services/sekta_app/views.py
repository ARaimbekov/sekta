from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .forms import UserLoginForm, RegisterForm, SektaCreationForm
from .models import Sektant, Sekta, Nickname
from .helpers import is_belong, encrypt, decrypt

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
    if request.user.dead:
        return HttpResponse(status=403, content='Вы мертвы')
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
    participants = [[sektant,[nickname.__str__() for nickname in Nickname.objects.filter(sektant=sektant)]] for sektant in Sektant.objects.all() if is_belong(sekta,sektant)]
    if request.user != sekta.creator and not is_belong(sekta,request.user):
        return HttpResponse(status=403, content='Вы не входите в секту')
    context={'sekta':sekta,'participants':participants}
    if request.user==sekta.creator and request.user.dead==False:
        context['creator']=True
    else:
        context['creator']=False
    return render(request,'sekta.html',context)

@login_required
def invite_sektant(request,id):
    try:
        follower = Sektant.objects.get(pk=int(request.GET.get('user')))
    except Sektant.DoesNotExist:
        return HttpResponse(status=400, content='Неверный id пользователя или секты')
    try:
        sekta = Sekta.objects.get(pk=int(request.GET.get('sect')))
    except Sekta.DoesNotExist:
        return HttpResponse(status=400, content='Неверный id пользователя или секты')
    new_name = request.GET.get('nickname')
    if request.user != sekta.creator:
        return HttpResponse(status=403, content='Вы не можете приглашать в чужую секту')
    if request.user.dead:
        return HttpResponse(status=403, content='Вы мертвы')
    if len(Nickname.objects.filter(sektant=follower).filter(sekta=sekta))>0:
        return HttpResponse(status=400, content='Этот пользователь уже в вашей секте')
    if follower.can_be_invited==False:
        return HttpResponse(status=400, content='Пользователь запретил себя приглашать')
    nickname = Nickname(sektant=follower,sekta=Sekta.objects.get(pk=id),nickname=encrypt((new_name).encode('utf-8'),Sekta.objects.get(pk=id).private_key))
    nickname.save()
    return HttpResponse(status=201, content=f'Сектант был успешно приглашен <a href="/sekta/{sekta.id}"><h3 class="panel-title">Назад в секту</h3></a>')

@login_required
def invite_to_sekta(request,id):
    try:
        sekta = Sekta.objects.get(pk=id)
    except Sekta.DoesNotExist:
        return HttpResponse(status=400, content='Неверный id пользователя или секты')
    if request.user != sekta.creator:
        return HttpResponse(status=403, content='Вы не можете приглашать в чужую секту')
    if request.user.dead:
        return HttpResponse(status=403, content='Вы мертвы')
    users = [user for user in Sektant.objects.filter(can_be_invited=True) if not is_belong(sekta,user) and user != sekta.creator]
    context = {'sekta':sekta,'users':users}
    return render(request, 'invitation.html', context)

@login_required
def sacrifice(request,id):
    try:
        sekta = Sekta.objects.get(pk=id)
    except Sekta.DoesNotExist:
        return HttpResponse(status=400, content='Неверный id пользователя или секты')
    if request.user != sekta.creator:
        return HttpResponse(status=403, content='Вы не можете совершать жертвоприношения в чужой секте')
    if request.user.dead:
        return HttpResponse(status=403, content='Вы мертвы')
    users = [user for user in Sektant.objects.filter(dead=False) if
              is_belong(sekta, user) and user != sekta.creator]
    context = {'sekta':sekta,'users':users}
    return render(request, 'sacrifice.html', context)

@login_required
def sacrifice_sektant(request,id):
    try:
        follower = Sektant.objects.get(pk=int(request.GET.get('user')))
    except Sektant.DoesNotExist:
        return HttpResponse(status=400, content='Неверный id пользователя или секты')
    try:
        sekta = Sekta.objects.get(pk=id)
    except Sekta.DoesNotExist:
        return HttpResponse(status=400, content='Неверный id пользователя или секты')
    if request.user != sekta.creator:
        return HttpResponse(status=403, content='Вы не можете совершать жертвоприношения в чужой секте')
    if request.user.dead:
        return HttpResponse(status=403, content='Вы мертвы')
    if follower.dead:
        return HttpResponse(status=400, content='Этот пользователь уже завершил земной путь')
    follower.dead=True
    nicknames=Nickname.objects.filter(sektant=follower)
    print(str(nicknames))
    for n in nicknames:
        print(str(n.nickname))
        sekta = n.sekta
        n.nickname=decrypt(n.nickname,sekta.private_key)
        print(str(n.nickname))
        n.save()
    follower.save()
    return HttpResponse(status=201, content=f'Сектант был успешно принесён в жертву <a href="/sekta/{sekta.id}"><h3 class="panel-title">Назад в секту</h3></a>')

