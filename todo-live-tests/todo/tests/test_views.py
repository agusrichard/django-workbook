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

    def test_negative_register_username_already_exists(self):
        self.test_positive_register_user_POST()

        response = self.client.post(
            self.register_url,
            data={"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.register_template)
        self.assertFormError(
            response, "form", "username", "A user with that username already exists."
        )

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
        self.create_todo_url = reverse("todo:create_todo")
        self.edit_todo_url = reverse("todo:edit_todo", args=["1"])
        self.delete_todo_url = reverse("todo:delete_todo", args=["1"])
        self.toggle_todo_url = reverse("todo:toggle_todo", args=["1"])
        self.register_template = "todo/register.html"
        self.login_template = "todo/login.html"
        self.home_template = "todo/home.html"
        self.create_todo_template = "todo/create_todo.html"
        self.edit_todo_template = "todo/edit_todo.html"

    def register(self):
        self.client.post(
            self.register_url,
            data={"username": "testuser", "password": "testpassword"},
        )

    def login(self):
        self.register()
        self.client.post(
            self.login_url,
            data={"username": "testuser", "password": "testpassword"},
        )

    def test_negative_home_user_not_logged_in(self):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.home_template)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_negative_create_todo_user_not_logged_in(self):
        response = self.client.get(reverse("todo:create_todo"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{self.login_url}?next={self.create_todo_url}")
        self.assertTemplateNotUsed(response, "todo/create_todo.html")

    def test_negative_edit_todo_user_not_logged_in(self):
        url = self.edit_todo_url
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{self.login_url}?next={url}")
        self.assertTemplateNotUsed(response, "todo/edit_todo.html")

    def test_positive_home_user_logged_in_empty_todos(self):
        self.login()

        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.home_template)
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(len(response.context["todos"]), 0)

    def test_positive_create_todo_GET(self):
        self.login()

        response = self.client.get(self.create_todo_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.create_todo_template)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_positive_create_todo_POST(self):
        self.login()

        response = self.client.post(
            self.create_todo_url,
            data={"title": "test title", "description": "test description"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)
        self.assertTemplateNotUsed(response, self.create_todo_template)

    def test_positive_edit_todo_GET(self):
        self.test_positive_create_todo_POST()

        response = self.client.get(self.edit_todo_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.edit_todo_template)
        self.assertTrue(response.context["user"].is_authenticated)

        self.assertEqual(response.context["form"].initial["title"], "test title")
        self.assertEqual(
            response.context["form"].initial["description"], "test description"
        )
        self.assertFalse(response.context["form"].initial["completed"])

    def test_positive_edit_todo_POST(self):
        self.test_positive_create_todo_POST()

        response = self.client.post(
            self.edit_todo_url,
            data={
                "title": "test title updated",
                "description": "test description updated",
                "completed": True,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)
        self.assertTemplateNotUsed(response, self.edit_todo_template)

        response = self.client.get(self.edit_todo_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.edit_todo_template)
        self.assertTrue(response.context["user"].is_authenticated)

        self.assertEqual(
            response.context["form"].initial["title"], "test title updated"
        )
        self.assertEqual(
            response.context["form"].initial["description"], "test description updated"
        )
        self.assertTrue(response.context["form"].initial["completed"])

    def test_negative_edit_todo_GET_not_found(self):
        self.test_positive_create_todo_POST()

        response = self.client.get(reverse("todo:edit_todo", args=["2"]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)
        self.assertTemplateNotUsed(response, self.edit_todo_template)

    def test_positive_delete_todo(self):
        self.test_positive_create_todo_POST()

        response = self.client.post(self.delete_todo_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)

        response = self.client.get(self.home_url)
        self.assertEqual(len(response.context["todos"]), 0)

    def test_negative_delete_todo_not_found(self):
        self.test_positive_create_todo_POST()

        response = self.client.get(reverse("todo:delete_todo", args=["2"]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)

    def test_positive_toggle_todo(self):
        self.test_positive_create_todo_POST()

        response = self.client.post(self.toggle_todo_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)

        response = self.client.get(self.home_url)
        self.assertEqual(len(response.context["todos"]), 1)
        self.assertTrue(response.context["todos"][0].completed)

    def test_negative_toggle_todo_not_found(self):
        self.test_positive_create_todo_POST()

        response = self.client.get(reverse("todo:toggle_todo", args=["2"]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)
