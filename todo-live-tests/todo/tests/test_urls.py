from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import home, register, login, logout


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
    pass
