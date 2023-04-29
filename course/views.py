from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.db.models import Count
import json

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
    print(lecture.rating)
    lecture.calculate_overall_rating()
    print(lecture.rating)
    width = ( lecture.rating / 5 ) * 100
    print(width)
    watched = Watched.objects.filter(lecture=lecture)
    notes = Note.objects.filter(lecture=lecture, user=request.user).order_by('-id')
    comments = Comment.objects.filter(lecture=lecture)
    userComment = Comment.objects.filter(lecture=lecture, user=request.user).first()


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
        "width": width,
        "watched": watched,
        "previous_lecture_id": previous_lecture_id,
        "next_lecture_id": next_lecture_id,
        "notes": notes,
        "comments": comments,
        "userComment": userComment,
    })


def create_note(request, course_id, lecture_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        desc = data.get('desc')
        noteId = data.get('noteId')
        lecture = Lecture.objects.get(id=lecture_id)

        if noteId:
            note = Note.objects.get(id=noteId)
            note.title = title
            note.desc = desc
            note.save()
        else: 
           Note.objects.create(lecture=lecture, user=request.user, title=title, desc=desc)
        
        return JsonResponse({'status': 'success'}, status=201)
    
    return JsonResponse(
        {'status': 'error', 
         'message': 'Invalid request method'}, 
         status=400)

def delete_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        noteId = data.get('noteId')

        note = Note.objects.get(id=noteId)
        print(note)
        note.delete()
        
        return JsonResponse({'status': 'success'}, status=201)
    
    return JsonResponse(
        {'status': 'error', 
         'message': 'Invalid request method'}, 
         status=400)

@enrolled_required
def review(request, course_id, lecture_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        lecture = Lecture.objects.get(id=lecture_id)

        cmnt = Comment.objects.filter(lecture=lecture, user=request.user).first()
        if cmnt:
            cmnt.rating = rating
            cmnt.comment = comment
            cmnt.is_edited = True
            cmnt.save()
        else:
            Comment.objects.create(lecture=lecture, user=request.user, rating=rating, comment=comment)
        
        return redirect(f'/course/{course_id}/lectures/{lecture_id}')
    
    return redirect(f'/course/{course_id}/lectures/{lecture_id}')
