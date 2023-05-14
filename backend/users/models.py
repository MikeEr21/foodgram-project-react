from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    GUEST: str = 'Гость'
    USER: str = 'Пользователь'
    ADMIN: str = 'Администратор'

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class User(AbstractUser):
    CHOICES = [
        (Role.GUEST, 'Гость'),
        (Role.USER, 'Пользователь'),
        (Role.ADMIN, 'Администратор'),
    ]
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Логин'
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=128,
        verbose_name='Пароль'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный'
    )
    role = models.CharField(
        max_length=150,
        choices=CHOICES,
        default=Role.GUEST,
        verbose_name='Права доступа'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]

    def __str__(self):
        return self.username

    def is_guest(self):
        return self.role == self.Role.GUEST

    @property
    def is_user(self):
        return self.role == self.Role.USER

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    @classmethod
    def create_user(cls, **kwargs):
        return cls(role=cls.Role.USER, **kwargs)

    class Meta:
        db_table = 'users'
        app_label = 'users'
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
