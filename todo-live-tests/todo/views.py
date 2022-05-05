from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import Todo
from .forms import UserForm, TodoForm
from .common import get_object_or_none

HOME_URL = "todo:home"


def home(request):
    if request.user.is_authenticated:
        todos = Todo.objects.filter(user=request.user)
        return render(request, "todo/home.html", {"todos": todos})

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
            return redirect(HOME_URL)

        form = UserForm()
        return render(
            request,
            "todo/login.html",
            {"error": "Invalid username or password.", "form": form},
        )

    form = UserForm()
    return render(request, "todo/login.html", {"form": form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("todo:login")


@login_required
def create_todo(request):
    if request.method == "POST":
        data = request.POST.copy()
        data["user"] = request.user
        form = TodoForm(data)
        if form.is_valid():
            form.save()
            return redirect(HOME_URL)
    else:
        form = TodoForm()

    return render(request, "todo/create_todo.html", {"form": form})


@login_required
def edit_todo(request, todo_id):
    todo = get_object_or_none(Todo, todo_id)
    if todo is None:
        return redirect(HOME_URL)

    if request.method == "POST":
        data = request.POST.copy()
        data["user"] = request.user
        form = TodoForm(data, instance=todo)
        if form.is_valid():
            form.save()
            return redirect(HOME_URL)
    else:
        form = TodoForm(instance=todo)

    return render(request, "todo/edit_todo.html", {"form": form})


@login_required
def delete_todo(_, todo_id):
    todo = get_object_or_none(Todo, todo_id)
    if todo is None:
        return redirect(HOME_URL)

    todo.delete()
    return redirect(HOME_URL)


@login_required
def toggle_todo(_, todo_id):
    todo = get_object_or_none(Todo, todo_id)
    if todo is None:
        return redirect(HOME_URL)

    todo.completed = not todo.completed
    todo.save()
    return redirect(HOME_URL)
