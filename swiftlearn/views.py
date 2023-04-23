from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.db.models import Count
import pycountry

from .models import *

# Create your views here.
def index(request):
    # get the top 3 courses based on the number of enrolled users
    courses = Course.objects.annotate(
        num_enrolled_users=Count('enroll', distinct=True)
    ).order_by('-num_enrolled_users')[:2]

    # add one paid course to the list
    paid_course = Course.objects.exclude(price=0).order_by('?').first()
    courses = list(courses) + [paid_course]

    return render(request, "swiftlearn/index.html", {
        'featuredCourses': courses,
    })



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



def course(request, course_id):
    course = Course.objects.get(id=course_id)
    instructors = course.instructor.all()
    try: enroll = Enroll.objects.get(course=course, user=request.user)
    except: enroll = None
    what_you_will_learn = course.what_you_will_learn.splitlines()
    return render(request, "swiftlearn/course.html", {
        "course": course,
        "instructors": instructors,
        "pointers": what_you_will_learn,
        "enroll": enroll,
    })



def instructor(request, instructor_id):
    instructor = Instructor.objects.get(id=instructor_id)
    return render(request, "swiftlearn/instructor.html", {
        "instructor": instructor,
    })



@login_required
def payment_and_enroll(request, course_id):
    course = Course.objects.get(id=course_id)

    if course.is_free:
        Enroll.objects.create(course=course, user=request.user)
        return redirect(f'/catalog/{course_id}')

    if request.method == 'POST' and (not course.is_free):
            # Perform payment logic here
            # NOTE: Not performing payment logic in this project
            Enroll.objects.create(course=course, user=request.user)
            return redirect(f'/catalog/{course_id}')

    COUNTRY_CHOICES = User.COUNTRY_CHOICES
    return render(request, 'swiftlearn/payment.html', {
        'course': course,
        'course_id': course_id,
        'COUNTRY_CHOICES': COUNTRY_CHOICES,
    })



@login_required
def validate_coupon(request):
    coupon_code = request.GET.get('code', None)
    if coupon_code:
        try: coupon = Coupon.objects.get(code=coupon_code)
        except: return JsonResponse({
            'valid': False,
            'error_message': 'Incorrect coupon code.',
        })
        if coupon.is_valid():
            return JsonResponse({
                'valid': True,
                'discount_percent': coupon.discount_percent,
            })
        else:
            return JsonResponse({
                'valid': False,
                'error_message': 'Coupon is no longer valid.',
            })
    else:
        return JsonResponse({
            'valid': False,
            'error_message': 'Coupon code is required.',
        })



@login_required
def dashboard(request):
    enrollments = Enroll.objects.filter(user=request.user)
    courses = [enroll.course for enroll in enrollments]

    # Check if the user has enrolled in only one category
    categories = Category.objects.filter(course__in=courses).distinct()
    if len(categories) == 1:
        rec_courses = Course.objects.filter(category=categories[0]).exclude(enroll__user=request.user)[:5]
    else:
        # User has enrolled in multiple categories
        rec_courses = []
        for category in categories:
            c = Course.objects.filter(category=category).exclude(enroll__user=request.user)[:1]
            rec_courses.extend(c)

        # If the number of recommended courses is less than 5, then recommend courses from any category
        num_rec_courses = len(rec_courses)
        if num_rec_courses < 5:
            additional_courses = Course.objects.exclude(enroll__user=request.user)[:5 - num_rec_courses]
            rec_courses.extend(additional_courses)

    # Remove duplicate courses from rec_courses
    rec_courses = list(set(rec_courses))

    return render(request, "swiftlearn/dashboard.html", {
        'courses': courses,
        'recommended_courses': rec_courses,
    })



@login_required
def profile(request):
    country_code = request.user.country
    country_name = pycountry.countries.get(alpha_2=country_code).name
    COUNTRY_CHOICES = User.COUNTRY_CHOICES
    return render(request, "swiftlearn/profile.html", {
        "country_name": country_name,
        'COUNTRY_CHOICES': COUNTRY_CHOICES,
    })



@login_required
def update_profile(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        country = request.POST["country"]

        user = User.objects.get(username=request.user)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.country = country
        user.save()

        return redirect("profile")



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
                "message": "Invalid username and/or password!"
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
        country = request.POST["country"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "swiftlearn/register.html", {
                "p_message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.country = country
            user.save()
        except IntegrityError:
            return render(request, "swiftlearn/register.html", {
                "u_message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        COUNTRY_CHOICES = User.COUNTRY_CHOICES
        return render(request, "swiftlearn/register.html", {
            "COUNTRY_CHOICES": COUNTRY_CHOICES,
        })

