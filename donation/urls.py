from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("home/", views.home, name="home"),
    path("donate-blood/", views.donate_blood, name="donate_blood"),
    path("request-blood/", views.request_blood, name="request_blood"),
    path("history/", views.history, name="history"),
    path("live-history/", views.live_history, name="live_history"),
]

