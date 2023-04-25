from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from swiftlearn.models import *

# Create your models here.
class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    link = models.URLField()
    rating = models.FloatField(default=0)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.course} - {self.title}"
    
    def calculate_overall_rating(self):
        total_rating = 0
        num_ratings = 0
        for comment in self.comments.all():
            total_rating += comment.rating
            num_ratings += 1
        if num_ratings > 0:
            self.rating = total_rating / num_ratings
            self.save()

    def get_num_ratings(self):
        num_ones = self.comments.filter(rating=1).count()
        num_twos = self.comments.filter(rating=2).count()
        num_threes = self.comments.filter(rating=3).count()
        num_fours = self.comments.filter(rating=4).count()
        num_fives = self.comments.filter(rating=5).count()
        return {
            '1': num_ones,
            '2': num_twos,
            '3': num_threes,
            '4': num_fours,
            '5': num_fives,
        }

    class Meta:
        verbose_name = "Lecture"
        verbose_name_plural = "Lectures"
        ordering = ['order']


class Comment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.username} - {self.lecture.title}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'lecture'),)
        verbose_name = 'Watched'
        verbose_name_plural = 'Watched'

    def __str__(self):
        return f"{self.user} - {self.lecture}"

class Note(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=40)
    desc = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        return f"{self.user} - {self.lecture} - {self.title}"

