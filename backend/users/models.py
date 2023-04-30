from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    GUEST: str = 'Гость'
    USER: str = 'Пользователь'
    ADMIN: str = 'Администратор'


class User(AbstractUser):
    CHOICES = [
        (Role.GUEST, 'Гость'),
        (Role.USER, 'Пользователь'),
        (Role.ADMIN, 'Администратор'),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
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
        return self.role == self.Role.ADMIN

    @classmethod
    def create_user(cls, **kwargs):
        return cls(role=cls.Role.USER, **kwargs)

    class Meta:
        db_table = 'users'
        app_label = 'users'
        ordering = ('id',)
