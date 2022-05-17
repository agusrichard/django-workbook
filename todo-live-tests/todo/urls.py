from django.urls import path

from .views import (
    home,
    login,
    logout,
    register,
    edit_todo,
    create_todo,
    delete_todo,
    toggle_todo,
)

app_name = "todo"

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_todo, name="create_todo"),
    path("edit/<int:todo_id>/", edit_todo, name="edit_todo"),
    path("delete/<int:todo_id>/", delete_todo, name="delete_todo"),
    path("toggle/<int:todo_id>/", toggle_todo, name="toggle_todo"),
    path("auth/register/", register, name="register"),
    path("auth/login/", login, name="login"),
    path("auth/logout/", logout, name="logout"),
]
