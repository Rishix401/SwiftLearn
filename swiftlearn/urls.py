from django.urls import path

from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("catalog", views.catalog, name="catalog"),
    path("category", views.category, name="category"),
    path("course/<int:id>", views.course, name="course"),
    path("instructor/<int:id>", views.instructor, name="instructor"),
    path("payment/<int:course_id>", views.payment_and_enroll, name="payment"),
    path("validate_coupon/", views.validate_coupon, name="validate_coupon"),
    path("dashboard", views.dashboard, name="dashboard"),
]