# Generated by Django 3.2.3 on 2024-06-16 13:06

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240613_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует.'}, help_text='Не более 150 символов. Только буквы,  цифры и @/./+/-/_', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Уникальный юзернейм'),
        ),
    ]
