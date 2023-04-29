from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),

    path("catalog", catalog, name="catalog"),
    path("category", category, name="category"),
    path("catalog/<int:course_id>", course, name="course"),
    path("instructor/<int:instructor_id>", instructor, name="instructor"),
    path("enroll/<int:course_id>", enroll, name="enroll"),
    path("dashboard", dashboard, name="dashboard"),
    path("profile", profile, name="profile"),
    path("update_profile", update_profile, name="update_profile"),

    path("create-checkout-session/<pk>/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("success/<course_id>/", successView, name="successView"),
    path("cancel/<course_id>/", cancelView, name="cancelView"),
    path('webhooks/stripe', stripe_webhook, name="stripe-webhook"),
    path('create-coupon/', create_coupon, name="create_coupon"),
]