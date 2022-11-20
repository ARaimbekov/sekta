from django.db import models
from django.contrib.auth.models import AbstractUser
from base64 import b64encode


class Sektant(AbstractUser):
    username = models.fields.CharField(max_length=50, unique=True)
    password = models.fields.CharField(max_length=128)
    dead = models.fields.BooleanField(default=False)
    can_be_invited = models.fields.BooleanField(default=True)

    def __str__(self):
        return self.username


class Sekta(models.Model):
    sektaname = models.fields.CharField(max_length=50,unique=True,verbose_name='Название секты')
    private_key = models.fields.BinaryField()
    creator = models.ForeignKey(Sektant,on_delete=models.CASCADE)
    description = models.CharField(max_length=140,blank=True,verbose_name='Описание секты (может быть пустым)')


    def __str__(self):
        return self.sektaname


class Nickname(models.Model):
    sektant = models.ForeignKey(Sektant, on_delete=models.CASCADE)
    sekta = models.ForeignKey(Sekta, on_delete=models.CASCADE)
    nickname = models.fields.BinaryField()

    def __str__(self):
        if self.sektant.dead == False:
            return b64encode(bytes(self.nickname))
        else:
            return (bytes(self.nickname)).decode('utf-8')

    class Meta:
        unique_together=['sektant','sekta']

class Vacancy(models.Model):
    sekta = models.ForeignKey(Sekta,on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    is_active = models.BooleanField()

