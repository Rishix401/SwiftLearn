from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.db.models import Count

from swiftlearn.models import *
from .models import *

# Create your views here.
@login_required
def course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    if Enroll.objects.get(user=request.user, course=course):
        print(Enroll.objects.get(user=request.user, course=course))
        return render(request, "course/coursePage.html", {
            "course": course,
        })