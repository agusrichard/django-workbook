from django.urls import path

from .views import home, register, login, logout

app_name = "todo"

urlpatterns = [
    path("", home, name="home"),
    path("auth/register/", register, name="register"),
    path("auth/login/", login, name="login"),
    path("auth/logout/", logout, name="logout"),
]
