from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):
    return render(request, "swiftlearn/index.html")


def catalog(request):
    categories = Category.objects.all()
    courses = Course.objects.all()

    selected_categories = request.GET.getlist('category')
    selected_status = request.GET.get('status')
    selected_min_price = request.GET.get('min_price')
    selected_max_price = request.GET.get('max_price')
    selected_is_free = request.GET.get('is_free')
    selected_is_paid = request.GET.get('is_paid')

    if selected_categories:
        courses = courses.filter(category__name__in=selected_categories)

    # filter courses based on selected status
    if selected_status:
        courses = courses.filter(status=selected_status)

    # filter courses based on selected price range
    if selected_max_price:
        courses = courses.filter(price__lte=selected_max_price)

    # filter courses based on selected is_free option
    if selected_is_free:
        courses = courses.filter(is_free=selected_is_free)

    context = {
        'categories': categories,
        'courses': courses,
        'selected_categories': selected_categories,
        'selected_status': selected_status,
        'selected_min_price': selected_min_price,
        'selected_max_price': selected_max_price,
        'selected_is_free': selected_is_free,
    }
    return render(request, 'swiftlearn/catalog.html', context)


def category(request):
    if request.method == "POST":
        categoryInp = request.POST['category']
        category = Category.objects.get(name=categoryInp)
        filterCourses = Course.objects.filter(category=category)
        allCats = Category.objects.all()
        return render(request, "swiftlearn/catalog.html", {
            "courses": filterCourses,
            "cats": allCats
        })


def course(request, id):
    course = Course.objects.get(id=id)
    instructors = course.instructor.all()
    try: enroll = Enroll.objects.get(course=course, user=request.user)
    except: enroll = ''
    what_you_will_learn = course.what_you_will_learn.splitlines()
    return render(request, "swiftlearn/course.html", {
        "course": course,
        "instructors": instructors,
        "pointers": what_you_will_learn,
        "enroll": enroll,
    })


def instructor(request, id):
    instructor = Instructor.objects.get(id=id)
    return render(request, "swiftlearn/instructor.html", {
        "instructor": instructor,
    })


@login_required
def payment(request):
    courseId = request.GET.get("course_id")
    print(courseId)
    if request.method == 'POST':
        enroll(request, courseId)

    user = request.user
    course = Course.objects.get(id=courseId, is_free=False)
    return render(request, "swiftlearn/payment.html", {
        "user": user,
        "course": course,
    })


@login_required
def enroll(request, course_id):
    # ensure that only free courses are enrolled through get request
    paidCourses = Course.objects.filter(is_free=False)
    for course in paidCourses:
        if course_id in course.id:
            print(course_id, course)
            print("true")
    else: print("false")
    # if request.method == 'POST':
    #     try: 
    #         courseId = request.POST.get("course_id")
    #         e = Enroll.objects.create(course=Course.objects.get(id=courseId), user=request.user)
    #     except: e = Enroll.objects.create(course=Course.objects.get(id=course_id), user=request.user)
    #     e.save()
    return redirect(f"/course/{courseId}")



@login_required
def dashboard(request):
    pass



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "swiftlearn/login.html", {
                "message": "Invalid email and/or password!"
            })
    else:
        return render(request, "swiftlearn/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            print("password must match.")
            return render(request, "swiftlearn/register.html", {
                "p_message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print("user created")
        except IntegrityError:
            print("username already taken.")
            return render(request, "swiftlearn/register.html", {
                "u_message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "swiftlearn/register.html")
