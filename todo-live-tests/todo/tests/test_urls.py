from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import (
    home,
    login,
    logout,
    register,
    edit_todo,
    create_todo,
    delete_todo,
    toggle_todo,
)


class TestUserUrl(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url = reverse("todo:home")
        self.assertEqual(resolve(url).func, home)

    def test_register_url_is_resolved(self):
        url = reverse("todo:register")
        self.assertEqual(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse("todo:login")
        self.assertEqual(resolve(url).func, login)

    def test_logout_url_is_resolved(self):
        url = reverse("todo:logout")
        self.assertEqual(resolve(url).func, logout)


class TestTodoUrl(SimpleTestCase):
    def test_create_todo_url_is_resolved(self):
        url = reverse("todo:create_todo")
        self.assertEqual(resolve(url).func, create_todo)

    def test_edit_todo_url_is_resolved(self):
        url = reverse("todo:edit_todo", kwargs={"todo_id": 1})
        self.assertEqual(resolve(url).func, edit_todo)

    def test_delete_todo_url_is_resolved(self):
        url = reverse("todo:delete_todo", kwargs={"todo_id": 1})
        self.assertEqual(resolve(url).func, delete_todo)

    def test_toggle_todo_url_is_resolved(self):
        url = reverse("todo:toggle_todo", kwargs={"todo_id": 1})
        self.assertEqual(resolve(url).func, toggle_todo)
