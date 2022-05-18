from .models import Sektant,Sekta,Nickname

def is_belong(sekta,sektant):
    participants = Nickname.objects.filter(sekta=sekta)
    for participant in participants:
        if participant.sektant == sektant:
            return True
    return False