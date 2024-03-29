# Sect service
Состоит из двух связанных сервисов:
- Sect (Python Django)
- Vacancies (Go)

Использует Postgres db \
Оба связанных сервиса запускаются вместе от одного docker compose файла
![My Image](scheme.png)

## Идея сервиса
Это сервис для ведения своей секты. Регистрируешься и можешь создавать свою секту, приглашать других юзеров или самому вступать в секту
Есть механика принесения своих последователей в жертву. Принесённый в жертву юзер считается мёртвым и не может больше совершать никаких действий
Есть отдельный сервис для выставления вакансии в свою секту. На вакансию можно откликнуться и получить специальный токен. Введя этот токен на основном сервисе, юзер может вступить в секту
Во время вступления в секту любым способом, юзеру даётся его новое секретное имя в этой секте. Его видит только создатель секты. Для остальных оно скрыто

## Места хранения флагов
Всего есть 2 места для хранения флагов:
1. Описание секты
2. Секретное имя сектанта

# Sekta (Django)
## Описание и функционал
При регистрации нового аккаунта есть выбор - разрешать приглашать себя в секты, или нет \
Любой зарегистрированный, но не принесённый в жертву пользователь, может создать секту, выбрав для неё название и описание \ 
После создания секты создатель может приглашать в неё других пользователей из числа тех, кто разрешил себя приглашать. \
При приглашении создатель секты пишет новое имя (секретное имя) для пользователя, которое затем шифруется AES \
После приглашения пользователь сразу добавляется в секту (подтверждение пользователя не нужно) \
На странице секты отображаются её создатель, описание и участники - отображается как юзернейм, так и секретное имя. У живых участников секретное имя отображается в зашифрованном виде. \
Создатель секты может принести пользователя-участника секты в жертву. При этом пользователь помечается как мертвый. \
Мертвый пользователь может просматривать свои секты, но не может создавать секты. Также его нельзя пригласить или принести в жертву.

## Детали реализации
Является REST-сервисом, работающим по http \
Страницы генерируются на стороне сервера с помощью Django темплейтов \

## Уязвимости
### 1. Вместо одного секретного имени отображается список всех секретных имён
На странице секты напротив сектанта вместо одного секретного имени, которое он получил в этой секте, отображается список всех секретных имён, полученных в разных сектах. Секретные имена других сект обёрнуты в тег с атрибутом `style:display=None` и не видны при просмотре страницы, но могут быть прочитаны в коде страницы. Если сектант состоит одновременно в секте1 и секте2, то при принесении его в жертву в секте1 все участники секты1 начнут видеть, какое секретное имя ему дали в секте2. Это позволит беспрепятственно получать флаги, которые хранятся в секретных именах создаваемых чекером сектантов.

**Косячный фрагмент**
```
participants = [
        (sektant, Nickname.objects.filter(sektant=sektant))
        for sektant in Sektant.objects.all() if is_belong(sekta, sektant)
        ]
```

**Пофикшенный фрагмент**
```
participants = [
        (sektant, Nickname.objects.filter(sektant=sektant).filter(sekta=sekta))
        for sektant in Sektant.objects.all() if is_belong(sekta, sektant)
        ]
```

### 2. Parameter pollution (в некотором роде) в функции приглашения сектанта
При приглашении в секту проверяется, что приглашающий пользователь является создателем секты. Но в запросе передаётся два параметра с id секты: проверяется, что пользователь является создателем первой секты (id в GET-параметре sect), но сектант приглашается во вторую (id в url). Это позволяет приглашать своего пользователя в чужую секту, чтобы посмотреть флаг, лежащий в описании

**Косячный фрагмент**
```
def invite_sektant(request, id):
    try:
        follower = Sektant.objects.get(pk=int(request.GET.get('user')))
    except Sektant.DoesNotExist:
        return render_helper(request, status=400, content='Неверный id пользователя или секты')
    try:
        sekta = Sekta.objects.get(pk=int(request.GET.get('sect')))
```

**Пофикшенный фрагмент**
```
def invite_sektant(request, id):
    try:
        follower = Sektant.objects.get(pk=int(request.GET.get('user')))
    except Sektant.DoesNotExist:
        return render_helper(request, status=400, content='Неверный id пользователя или секты')
    try:
        sekta = Sekta.objects.get(pk=id)
```


# Vacancies (Go)
## Описание и функционал
**Сервис не содержит флагов** \
Позволяет создавать вакансию для вступления в свою секту \
Для одной секты создаётся одна вакансия \
Если юзер откликается на вакансию, то он получает специальный токен, который можно ввести на Django сервисе, чтобы вступить в секту \
Создатель секты может посмотреть токен на странице своей секты \
Откликнуться на вакансию можно только если она активна \
Делать вакансию активной или не активной может только владелец секты


## Детали реализации
Сервис реализует общение с клиентом при помощи GRPC \
Сервис связан с основным сервисом на Django только через бд

Для общения с сервисом можно использовать следующие GRPC-клиенты
- CLI [Evans](https://github.com/ktr0731/evans)
- GUI [BloomRPC](https://github.com/bloomrpc/bloomrpc/releases) (проще всего поставить как AppImage)

## Доступные действия
1. Создать новую вакансию
2. Просмотреть список последних сорока вакансий
3. Откликнуться на вакансию / просмотреть одну
4. Редактировать свою вакансию

## Уязвимости
### 1. Создание своей вакансии на чужую секту
В методе `Service.Create` нет проверки на то, что вакансия для конкретной секты уже была создана \
Это позволяет создать свою вакансию и получить от неё токен

**Косячный фрагмент**
```
if errors.Is(err, ErrNotFound) {
    err = nil
}
if err != nil {
	return
}
```

**Пофикшенный фрагмент**
```
if err == nil {
	err = errors.New("already exist")
	return
}

if !errors.Is(err, ErrNotFound) {
	return
}
```

### 2. При редактировании можно просмотреть всю информацию о чужой вакансии (включая токен)
В методе `Service.Edit` сначала берётся вакансия из бд, а потом идёт проверка, передал ли юзер правильный токен, чтобы он мог её редактировать
Уязвимость в том, что создаётся переменная `ErrNotOwner`, но она не возвращается. Возвращается целиком структура вакансии `v` и `err` (которая  в тот момент имеет значение `nil`), следовательно юзер получит всю структуру без ошибки

**Косячный фрагмент**
```
if dto.Token != v.Token {
	ErrNotOwner = errors.New("not owner")
	return
}
```

**Пофикшенный фрагмент**
```
if dto.Token != v.Token {
	err = ErrNotOwner
	return
}
```

### 3. SQL - инъекция
В методе `Storage.Get` строится sql запрос
Если закомментить фрагмент `and is_active = true`, то вакансия с токеном будет показываться даже если она не активна


# Checker
Есть два чекера на два места хранения флагов: 
1. Секретные имена сектантов `checker_flagstorage_1.py`
2. Описание секты `checker_flagstorage_2.py`
