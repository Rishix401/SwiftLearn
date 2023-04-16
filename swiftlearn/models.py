from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=4000)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('upcoming', 'Upcoming'),
    )
    DIFFICULTY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=4000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_free = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    date = models.DateField()
    duration = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)

    what_you_will_learn = models.TextField(blank=True)
    course_language = models.CharField(max_length=50)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    instructor = models.ManyToManyField(Instructor, related_name='courses')

    def __str__(self):
        return self.title
