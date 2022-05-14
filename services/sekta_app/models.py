from django.db import models
from django.contrib.auth.models import AbstractUser


class Sektant(AbstractUser):
    username = models.fields.CharField(max_length=50,unique=True)
    password = models.fields.CharField(max_length=128)
    dead = models.fields.BooleanField(default=False)

    def __str__(self):
        return self.username


class Sekta(models.Model):
    sektaname = models.fields.CharField(max_length=50,unique=True)
    private_key = models.fields.CharField(max_length=32)
    creator = models.ForeignKey(Sektant,on_delete=models.CASCADE)

    def __str__(self):
        return self.sektaname


class Nickname(models.Model):
    sektant = models.OneToOneField(Sektant,on_delete=models.CASCADE)
    sekta = models.OneToOneField(Sekta,on_delete=models.CASCADE)
    nickname = models.fields.CharField(max_length=50)

    def __str__(self):
        return self.nickname


