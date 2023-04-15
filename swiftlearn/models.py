from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('upcoming', 'Upcoming'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_free = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    date = models.DateField()
    duration = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
