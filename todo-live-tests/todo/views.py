from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .forms import UserForm


def home(request):
    return render(request, "todo/home.html")


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todo:login")
    else:
        form = UserForm()

    return render(request, "todo/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("todo:home")
        else:
            return render(
                request, "todo/login.html", {"error": "Invalid username or password."}
            )
    else:
        form = UserForm()

    return render(request, "todo/login.html", {"form": form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("todo:login")
