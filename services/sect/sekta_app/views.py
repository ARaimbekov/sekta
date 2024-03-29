from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import (RegisterForm, SektaCreationForm, TokenInputForm,
                    UserLoginForm)
from .helpers import is_belong
from .models import Nickname, Sekta, Sektant, Vacancy


def home(request):
    return render(request, 'home.html', {})


def register(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegisterForm()

    context['form'] = form
    return render(request, 'register.html', context)


def login(request):
    context = {}
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
def logout(request):
    auth.logout(request)
    return redirect('/welcome/')


@login_required
def list_user_sekts(request):
    user_sekts = Sekta.objects.filter(creator=request.user)
    member_sekts = [
        nickname.sekta for nickname in Nickname.objects.filter(sektant=request.user)]
    context = {'user_sekts': user_sekts,
               'member_sekts': member_sekts,
               'user': request.user}
    return render(request, 'user_sekts_list.html', context)


@login_required
def list_all_sekts(request):
    sekts = Sekta.objects.all().order_by('-id')
    paginator = Paginator(sekts, 13)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'all_sekts_list.html', {'page_obj': page_obj, 'user': request.user})


@login_required
def create_sekta(request):
    if request.user.dead:
        return render_helper(request, status=403, content='Вы мертвы')

    if request.method == 'GET':
        form = SektaCreationForm()
        return render(request, 'create_sekta.html', {'form': form, 'user': request.user})

    if request.method == 'POST':
        form = SektaCreationForm(data=request.POST)
        if not form.is_valid():
            return render_helper(request, status=400, content='Секта с таким именем уже есть')

        sekta = form.save(request.user)
        return redirect(f'/sekta/{sekta.id}')


@login_required
def show_sekta(request, id):
    sekta = Sekta.objects.get(pk=id)
    participants = [
        (sektant, Nickname.objects.filter(sektant=sektant))
        for sektant in Sektant.objects.all() if is_belong(sekta, sektant)
        ]

    if request.user != sekta.creator and not is_belong(sekta, request.user):
        return render_helper(request, status=403, content='Вы не входите в секту')

    vacancy = Vacancy.objects.filter(sekta_id=sekta.id).first()

    is_creator = request.user == sekta.creator and request.user.dead == False

    context = {
        'sekta': sekta,
        'participants': participants,
        'user': request.user,
        'token': vacancy.token if vacancy != None else None,
        'creator': is_creator,
    }

    return render(request, 'sekta.html', context)


@ login_required
def invite_sektant(request, id):
    try:
        follower = Sektant.objects.get(pk=int(request.GET.get('user')))
    except Sektant.DoesNotExist:
        return render_helper(request, status=400, content='Неверный id пользователя или секты')
    try:
        sekta = Sekta.objects.get(pk=int(request.GET.get('sect')))
    except Sekta.DoesNotExist:
        return render_helper(request, status=400, content='Неверный id пользователя или секты')
    new_name = request.GET.get('nickname')
    if request.user != sekta.creator:
        return render_helper(request, status=403, content='Вы не можете приглашать в чужую секту')
    if request.user.dead:
        return render_helper(request, status=403, content='Вы мертвы')
    if len(Nickname.objects.filter(sektant=follower).filter(sekta=sekta)) > 0:
        return render_helper(request, status=400, content='Этот пользователь уже в вашей секте')
    if follower.can_be_invited == False:
        return render_helper(request, status=400, content='Пользователь запретил себя приглашать')
    if follower.dead:
        return render_helper(request, status=400, content='Этот пользователь уже завершил земной путь')
    if follower == request.user:
        return render_helper(request, status=400, content='Вы не можете пригласить сами себя')
    nickname = Nickname(
        sektant=follower, 
        sekta=Sekta.objects.get(pk=id), 
        nickname=new_name)
    nickname.save()
    return render_helper(request, status=201, content=f'Сектант был успешно приглашен <a href="/sekta/{sekta.id}"><h3 class="panel-title">Назад в секту</h3></a>')


@ login_required
def invite_to_sekta(request, id):
    try:
        sekta = Sekta.objects.get(pk=id)
    except Sekta.DoesNotExist:
        return render_helper(request, status=400, content='Неверный id пользователя или секты')
    if request.user != sekta.creator:
        return render_helper(request, status=403, content='Вы не можете приглашать в чужую секту')
    if request.user.dead:
        return render_helper(request, status=403, content='Вы мертвы')
    users = [user for user in Sektant.objects.filter(can_be_invited=True) if not is_belong(
        sekta, user) and user != sekta.creator and not user.dead]
    paginator = Paginator(users, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'sekta': sekta, 'page_obj': page_obj, 'user': request.user}
    return render(request, 'invitation.html', context)


@ login_required
def sacrifice(request, id):
    try:
        sekta = Sekta.objects.get(pk=id)
    except Sekta.DoesNotExist:
        return render_helper(request, status=400, content='Неверный id пользователя или секты')
    if request.user != sekta.creator:
        return render_helper(request, status=403, content='Вы не можете совершать жертвоприношения в чужой секте')
    if request.user.dead:
        return render_helper(request, status=403, content='Вы мертвы')
    users = [user for user in Sektant.objects.filter(dead=False) if
             is_belong(sekta, user) and user != sekta.creator]
    paginator = Paginator(users, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'sekta': sekta, 'page_obj': page_obj, 'user': request.user}
    return render(request, 'sacrifice.html', context)


@ login_required
def sacrifice_sektant(request, id):
    try:
        follower = Sektant.objects.get(pk=int(request.GET.get('user')))
    except Sektant.DoesNotExist:
        return render_helper(request, status=400, content='Неверный id пользователя или секты')
    try:
        sekta = Sekta.objects.get(pk=id)
    except Sekta.DoesNotExist:
        return render_helper(request, status=400, content='Неверный id пользователя или секты')
    if not is_belong(sekta, follower):
        return render_helper(request, status=403, content='Этот пользователь не состоит в вашей секте')
    if request.user != sekta.creator:
        return render_helper(request, status=403, content='Вы не можете совершать жертвоприношения в чужой секте')
    if request.user.dead:
        return render_helper(request, status=403, content='Вы мертвы')
    if follower.dead:
        return render_helper(request, status=400, content='Этот пользователь уже завершил земной путь')
    follower.dead = True
    follower.save()
    return render_helper(request, status=201, content=f'Сектант был успешно принесён в жертву <a href="/sekta/{sekta.id}"><h3 class="panel-title">Назад в секту</h3></a>')


@ login_required
def join_by_token(request):
    if request.method == 'GET':
        form = TokenInputForm
        return render(request, 'token_input.html', {'form': form})
    else:
        form = TokenInputForm(data=request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            sekta = form.cleaned_data['sekta']

        if len(Vacancy.objects.filter(Q(token=token) & Q(sekta=sekta))):
            if not len(Nickname.objects.filter(Q(sekta=sekta) & Q(sektant=request.user))):
                form.save(request.user)
                return redirect(f'/sekta/{sekta.id}')
            else:
                return render_helper(request, status=400, content='Вы уже состоите в данной секте')
        else:
            return render_helper(request, status=400, content='Токен не подходит')


def render_helper(request, status, content):
    return render(request, 'helper.html', context={'text': content}, status=status)
