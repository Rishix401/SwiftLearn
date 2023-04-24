from django.contrib import admin

from .models import *

# Register your models here.
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'rating')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecture', 'comment', 'rating')
    search_fields = ('user__username', 'lecture__title')
    list_filter = ('rating', 'lecture__course')

class WatchedAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecture')
    search_fields = ('user__username', 'lecture__title')
    list_filter = ('lecture__course',)

admin.site.register(Lecture, LectureAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watched, WatchedAdmin)