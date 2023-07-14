from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    password_confirmation = models.CharField(max_length=128, default='')

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'Username: {self.username} Email: {self.email} Password: {self.password}'