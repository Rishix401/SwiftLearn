from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

from decimal import Decimal
import json
import pycountry
import stripe
import uuid

from .models import *


# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY

# check if user is subscribed to email or not
def check_email_subscribe(request):
    try: 
        if Email.objects.get(user=request.user): 
            return True 
    except: 
        return False 

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
        'email_subscribed': check_email_subscribe(request),
    })



def catalog(request):
    categories = Category.objects.all()
    courses = Course.objects.all()

    selected_categories = request.GET.getlist('category')
    selected_status = request.GET.get('status')
    selected_max_price = request.GET.get('max_price')
    selected_is_free = request.GET.get('is_free')

    if selected_categories:
        courses = courses.filter(category__name__in=selected_categories)

    # filter courses based on selected status
    if selected_status:
        courses = courses.filter(status=selected_status)

    # filter courses based on selected price range
    if selected_max_price:
        selected_max_price_in_cents = int(Decimal(selected_max_price) * 100)
        courses = courses.filter(price__lte=selected_max_price_in_cents)

    # filter courses based on selected is_free option
    if selected_is_free:
        courses = courses.filter(is_free=selected_is_free)

    context = {
        'categories': categories,
        'courses': courses,
        'selected_categories': selected_categories,
        'selected_status': selected_status,
        'selected_max_price': selected_max_price,
        'selected_is_free': selected_is_free,
        'email_subscribed': check_email_subscribe(request),
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
        'email_subscribed': check_email_subscribe(request),
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    })



def instructor(request, instructor_id):
    instructor = Instructor.objects.get(id=instructor_id)
    return render(request, "swiftlearn/instructor.html", {
        "instructor": instructor,
    })



@staff_member_required
def create_coupon(request):
    if request.method == 'POST':
        # Get the coupon data from the request
        code = request.POST.get('code')
        percent_off = request.POST.get('percent_off')
        duration = request.POST.get('duration')
        duration_in_months = request.POST.get('duration_in_months')
        redeem_by = request.POST.get('redeem_by')
        
        # Create a Coupon object in the database
        coupon = Coupon(
            code=code,
            percent_off=percent_off,
            duration=duration,
            duration_in_months=duration_in_months if duration_in_months else None,
            redeem_by=redeem_by if redeem_by else None,
        )
        coupon.save()
        
        # Create the coupon in Stripe
        try:
            coupon = stripe.Coupon.retrieve(code)
        except stripe.error.InvalidRequestError:
            if duration == 'once' or duration == 'forever':
                coupon = stripe.Coupon.create(
                    id=code,
                    percent_off=percent_off,
                    duration=duration,
                    redeem_by=redeem_by.timestamp() if redeem_by else None
                )
            else:
                coupon = stripe.Coupon.create(
                    id=code,
                    percent_off=percent_off,
                    duration=duration,
                    duration_in_months=duration_in_months,
                    redeem_by=redeem_by.timestamp() if redeem_by else None
                )

        # Create the promotion code in Stripe
        promotion_code = stripe.PromotionCode.create(
            coupon=code,
            code=code
        )
        return JsonResponse({'success': True})

    return render(request, 'swiftlearn/create_coupon.html')



def successView(request, course_id):
    return render(request, "swiftlearn/success.html", { "course_id": course_id, })

def cancelView(request, course_id):
        return render(request, "swiftlearn/cancel.html", { "course_id": course_id, })


# stripe listen --forward-to localhost:8000/webhooks/stripe
class CreateCheckoutSessionView(generic.View):
    def post(self, request, *args, **kwargs):
        course_id = self.kwargs["pk"]

        course = Course.objects.get(id=course_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': course.price,
                        'product_data': {
                            'name': course.title,
                            'images': [course.image_url],
                        }
                        },
                    'quantity': 1,
                },
            ],
            metadata={
                "course_id": course.id,
                "user_id": request.user.id,
            },
            mode='payment',
            allow_promotion_codes= True,
            invoice_creation={"enabled": True},
            success_url=YOUR_DOMAIN + f'/success/{course.id}/',
            cancel_url=YOUR_DOMAIN + f'/cancel/{course.id}/',
        )

        return JsonResponse({
            'id': checkout_session.id,
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(staus=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase
        customer_email = session["customer_details"]["email"]
        course_id = session["metadata"]["course_id"]
        user_id = session["metadata"]["user_id"]

        course = Course.objects.get(id=course_id) # Get the course object
        user = User.objects.get(id=user_id) # Get the user object
        Enroll.objects.create(course=course, user=user) # Enroll the user in course

        send_mail(
            f"Congrats! You're enrolled in {course.title}",
            f"Thanks for your purchase! Start Learning: http://127.0.0.1:8000/course/{course_id}",
            settings.EMAIL_HOST_USER,
            [customer_email],
            fail_silently=False
        )

    return HttpResponse(status=200)


@login_required
def enroll(request, course_id):
    course = Course.objects.get(id=course_id)

    if course.is_free:
        Enroll.objects.create(course=course, user=request.user)
        
        send_mail(
            f"Congrats! You're enrolled in {course.title}",
            f"Thanks for your enrollment! Start Learning: http://127.0.0.1:8000/course/{course_id}",
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False
        )
        
        return redirect(f'/catalog/{course_id}')
    

def counseling(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        mobile_number = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")


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
        'email_subscribed': check_email_subscribe(request),
    })


@login_required
def email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        Email.objects.create(email=email)
        send_mail("Swiftlearn email subscribed", 
            "you have successfully subscribed our email.", 
            settings.EMAIL_HOST_USER, [email], 
            fail_silently=False
        )
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failed'})


@staff_member_required
def send_mail_to_all_subscribers(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = Email.objects.values_list('email', flat=True)
    
        # Send email to each recipient
        for recipient in recipient_list:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

        # Return a success response
        return HttpResponse("Email sent to all users!")
   
    return render(request, "swiftlearn/sendMail.html")


@login_required
def profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # Check if the new passwords match
        if new_password != confirm_password:
            return JsonResponse({'success': False, 'error': "New passwords don't match!"})
        
        # Check if the old password is correct
        user = authenticate(username=request.user.username, password=old_password)
        if user is None:
            return JsonResponse({'success': False, 'error': "Old password is incorrect!"})
        
        # Update the password in the database
        user.set_password(new_password)
        user.save()
        
        return JsonResponse({'success': True})

    country_code = request.user.country
    try: country_name = pycountry.countries.get(alpha_2=country_code).name
    except: country_name = None
    
    COUNTRY_CHOICES = User.COUNTRY_CHOICES
    return render(request, "swiftlearn/profile.html", {
        "country_name": country_name,
        'COUNTRY_CHOICES': COUNTRY_CHOICES,
        'email_subscribed': check_email_subscribe(request),
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

    
def change_password(request, token):
    context = {"token": token}
    try:
        profile_obj = Profile.objects.get(forget_password_token=token)

        if request.method == "POST":
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            user_id = request.POST.get("user_id")

            if user_id is None:
                return redirect('/change-password/{token}')
                
            if new_password != confirm_password:
                return JsonResponse({"status": "failed"})
            
            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()

            profile_obj.forget_password_token = ''
            profile_obj.save()

            return JsonResponse({"status": "success"})

        context = {"user_id": profile_obj.user.id, "token": token}
        

    except Exception as e:
        print(e)
    return render(request, "swiftlearn/changePassword.html", context)


def send_forget_pass_mail(email, token):
    subject = 'Swiftlearn: Forgotten Password'
    message = '''
    Hello

    You have requested a new password for your Swiftlearn account.

    Click the following link to reset your password:

    http://127.0.0.1:8000/change-password/{}

    Thank you,

    The Swiftlearn team
    http://127.0.0.1:8000/
    '''.format(token)

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return True


def forget_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                return JsonResponse({"message": "No user found with this username.", "status": "failed"}, status=200)
            
            User_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            Profile_obj = Profile.objects.get(user=User_obj)
            Profile_obj.forget_password_token = token
            Profile_obj.save()
            
            send_forget_pass_mail(User_obj.email, token)
            return JsonResponse({"message": "Change Password link sent to your email.", "status": 'success'}, status=200)

    except Exception as e:
        print(e)

    return redirect('/login')


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

            profile = Profile.objects.create(user=user)
            profile.save()

        except IntegrityError:
            return render(request, "swiftlearn/register.html", {
                "u_message": "Username already taken."
            })
        
        login(request, user)
        send_mail(
            "Swiftlearn: New Account Created",
            "Congrats! you have successfully created a swiftlearn account. Start Learning: http://127.0.0.1:8000",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return HttpResponseRedirect(reverse("index"))
    else:
        COUNTRY_CHOICES = User.COUNTRY_CHOICES
        return render(request, "swiftlearn/register.html", {
            "COUNTRY_CHOICES": COUNTRY_CHOICES,
        })

