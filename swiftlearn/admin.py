from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'title',)
    search_fields = ('name',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'start_date', 'end_date',)
    list_filter = ('status', 'category',)
    search_fields = ('title', 'category__name',)
    filter_horizontal = ('instructor',)

class EnrollAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'enrollment_date', 'certificate',)
    list_filter = ('certificate',)
    search_fields = ('course__title', 'user__username',)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to',)
    search_fields = ('code',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'rating',)
    search_fields = ('title', 'course__title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecture', 'comment', 'rating',)
    search_fields = ('user__username', 'lecture__title',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enroll, EnrollAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)