from django.urls import reverse
from django.test import Client, TestCase


REQUIRED_FIELD_ERROR = "This field is required."


class TestUserView(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("todo:register")
        self.login_url = reverse("todo:login")
        self.logout_url = reverse("todo:logout")
        self.home_url = reverse("todo:home")
        self.register_template = "todo/register.html"
        self.login_template = "todo/login.html"

    def test_register_user_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.register_template)

    def test_positive_register_user_POST(self):
        response = self.client.post(
            self.register_url,
            data={"username": "testuser", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)
        self.assertTemplateNotUsed(response, self.register_template)

    def test_negative_register_user_POST_empty_data(self):
        response = self.client.post(
            self.register_url, data={"username": "", "password": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.register_template)
        self.assertFormError(response, "form", "username", REQUIRED_FIELD_ERROR)
        self.assertFormError(response, "form", "password", REQUIRED_FIELD_ERROR)

    def test_negative_register_user_POST_empty_username(self):
        response = self.client.post(
            self.register_url, data={"username": "", "password": "testpassword"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.register_template)
        self.assertFormError(response, "form", "username", REQUIRED_FIELD_ERROR)
        self.assertFalse("password" in response.context["form"].errors)

    def test_negative_register_user_POST_empty_password(self):
        response = self.client.post(
            self.register_url, data={"username": "testuser", "password": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.register_template)
        self.assertFalse("username" in response.context["form"].errors)
        self.assertFormError(response, "form", "password", REQUIRED_FIELD_ERROR)

    def test_login_user_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)

    def test_negative_login_user_POST_user_not_found(self):
        response = self.client.post(
            self.login_url,
            data={"username": "testuser", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)
        self.assertEqual(response.context["error"], "Invalid username or password.")

    def test_positive_login_user_POST(self):
        self.test_positive_register_user_POST()

        response = self.client.post(
            self.login_url,
            data={"username": "testuser", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)
        self.assertTemplateNotUsed(response, self.login_template)

    def test_not_logged_in_user_is_not_authenticated(self):
        response = self.client.get(self.home_url)

        self.assertFalse(response.context["user"].is_authenticated)

    def test_logged_in_user_is_authenticated(self):
        self.test_positive_login_user_POST()

        response = self.client.get(self.home_url)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_logout_user(self):
        self.test_positive_login_user_POST()

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)


class TestTodoView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.register_url = reverse("todo:register")
        self.login_url = reverse("todo:login")
        self.logout_url = reverse("todo:logout")
        self.home_url = reverse("todo:home")
        self.register_template = "todo/register.html"
        self.login_template = "todo/login.html"

    def test_home(self):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/home.html")
