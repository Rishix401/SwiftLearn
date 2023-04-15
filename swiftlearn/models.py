from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users'
    )

