from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

from .constants import (EMAIL_MAX_LENGTH, FIRST_NAME_MAX_LENGTH,
                        LAST_NAME_MAX_LENGTH, USERNAME_MAX_LENGTH)


class MyUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        blank=False,
        help_text=('Не более 150 символов. Только буквы,  '
                   'цифры и @/./+/-/_'),
        validators=[UnicodeUsernameValidator(), ],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    first_name = models.CharField(
        'Имя',
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=LAST_NAME_MAX_LENGTH,
        blank=False
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
        blank=False,
        max_length=EMAIL_MAX_LENGTH
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='users/avatars/',
        default=None,
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    subscriptions = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписки'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscriptions'],
                name='unique_user_subscriptions'
            )
        ]

    def clean(self):
        if self.user == self.subscriptions:
            raise ValidationError('Нельзя подписаться на самого себя.')
