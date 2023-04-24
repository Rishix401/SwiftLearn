from django.urls import path

from .import views

urlpatterns = [
    path("course/<int:course_id>", views.course_view, name="course_detail"),
    path("course/<int:course_id>/lectures/<int:lecture_id>", views.lecture, name="lecture"),
]