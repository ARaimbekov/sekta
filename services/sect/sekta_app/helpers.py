from .models import Nickname


def is_belong(sekta, sektant):
    if len(Nickname.objects.filter(sekta=sekta).filter(sektant=sektant)):
        return True
    return False
