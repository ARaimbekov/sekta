# Generated by Django 3.2.13 on 2022-05-20 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sekta_app', '0002_sektant_can_be_invited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nickname',
            name='sekta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sekta_app.sekta'),
        ),
        migrations.AlterField(
            model_name='nickname',
            name='sektant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='nickname',
            unique_together={('sektant', 'sekta')},
        ),
    ]
