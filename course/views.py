from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.db.models import Count

from swiftlearn.models import *
from .models import *


def enrolled_required(view_func):
    def wrapped_view(request, course_id, *args, **kwargs):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return HttpResponseForbidden()
        
        if not Enroll.objects.filter(user=request.user, course=course).exists():
            return HttpResponseForbidden()

        return view_func(request, course_id, *args, **kwargs)
    
    return wrapped_view


# Create your views here.
@enrolled_required
def course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    lectures = Lecture.objects.filter(course=course)
    watched = Watched.objects.filter(user=request.user, lecture__in=lectures)
    watched_lectures = [watched_item.lecture for watched_item in watched]
    return render(request, "course/coursePage.html", {
            "course": course,
            "lectures": lectures,
            "watched_lectures": watched_lectures,
    })


@enrolled_required
def lecture(request, course_id, lecture_id):
    course = Course.objects.get(id=course_id)
    lecture = Lecture.objects.get(id=lecture_id)
    watched = Watched.objects.filter(lecture=lecture)

    try:
        previous_lecture_id = Lecture.objects.filter(course=course, order__lt=lecture.order).order_by('-order')[0].id
    except IndexError:
        previous_lecture_id = None

    try:
        next_lecture_id = Lecture.objects.filter(course=course, order__gt=lecture.order).order_by('order')[0].id
    except IndexError:
        next_lecture_id = None

    if request.method == 'POST':
        if not watched:
            Watched.objects.create(user=request.user, lecture=lecture)
    
    return render(request, "course/lecture.html", {
        "course": course,
        "lecture": lecture,
        "watched": watched,
        "previous_lecture_id": previous_lecture_id,
        "next_lecture_id": next_lecture_id,
    })