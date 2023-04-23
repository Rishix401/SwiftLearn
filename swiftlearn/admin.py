from django.contrib import admin

from .models import *

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

# Register your models here.
admin.site.register(User)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Enroll)
admin.site.register(Coupon)
admin.site.register(Cart)