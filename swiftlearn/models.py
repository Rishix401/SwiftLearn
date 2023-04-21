from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=4000)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"


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
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)

    what_you_will_learn = models.TextField(blank=True)
    course_language = models.CharField(max_length=50)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    instructor = models.ManyToManyField(Instructor, related_name='courses')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Enroll(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(default=timezone.now)
    certificate = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f"{self.user.username}'s cart"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveSmallIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now and self.valid_to >= now

    def discount_amount(self, total_price):
        return (self.discount_percent / 100) * total_price

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
