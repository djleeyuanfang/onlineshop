from django.urls import path
from . import views

app_name = "mAuth"

urlpatterns = [
    path("", views.login),
    path("register/", views.register),
    path("out/", views.logout),
    path("mail_code/", views.send_mail_code)
]