# Generated by Django 3.2.4 on 2022-06-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sekta_app', '0005_alter_nickname_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nickname',
            name='nickname',
            field=models.BinaryField(),
        ),
    ]
