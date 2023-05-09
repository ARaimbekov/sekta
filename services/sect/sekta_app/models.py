from django.db import models
from django.contrib.auth.models import AbstractUser
from .aes_init import encrypt


class Sektant(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    dead = models.BooleanField(default=False)
    can_be_invited = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Sekta(models.Model):
    sektaname = models.CharField(
        max_length=70, unique=True, verbose_name='Название секты')
    private_key = models.BinaryField()
    creator = models.ForeignKey(Sektant, on_delete=models.CASCADE)
    description = models.CharField(
        max_length=140, blank=True, verbose_name='Описание секты (может быть пустым)')
    can_has_vacancy = models.BooleanField(default=True)

    def __str__(self):
        return self.sektaname


class Nickname(models.Model):
    sektant = models.ForeignKey(Sektant, on_delete=models.CASCADE)
    sekta = models.ForeignKey(Sekta, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    encrypted_nickname = models.CharField(max_length=70)

    def save(self, *args, **kwargs):
        self.encrypted_nickname = encrypt((self.nickname).encode('utf-8'), self.sekta.private_key)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.sektant.dead:
            return self.nickname
        else:
            return self.encrypted_nickname

    class Meta:
        unique_together = ['sektant', 'sekta']


class Vacancy(models.Model):
    sekta = models.ForeignKey(Sekta, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    is_active = models.BooleanField()
