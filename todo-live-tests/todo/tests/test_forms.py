from django.test import TestCase
from django.contrib.auth.models import User

from todo.models import Todo

from ..forms import UserForm, TodoForm

REQUIRED_FIELD_ERROR = "This field is required."


class TestUserForm(TestCase):
    def test_negative_register_empty_data_is_valid(self):
        form = UserForm()
        self.assertFalse(form.is_valid())

    def test_negative_register_empty_data_error_message(self):
        form = UserForm(data={"username": "", "password": ""})
        self.assertEqual(form.errors["username"][0], REQUIRED_FIELD_ERROR)
        self.assertEqual(form.errors["password"][0], REQUIRED_FIELD_ERROR)

    def test_negative_register_empty_username_is_valid(self):
        form = UserForm(data={"username": "", "password": "testpassword"})
        self.assertFalse(form.is_valid())

    def test_negative_register_empty_username_error_message(self):
        form = UserForm(data={"username": "", "password": "testpassword"})
        self.assertEqual(form.errors["username"][0], REQUIRED_FIELD_ERROR)

    def test_negative_register_empty_password_is_valid(self):
        form = UserForm(data={"username": "testuser", "password": ""})
        self.assertFalse(form.is_valid())

    def test_negative_register_empty_password_error_message(self):
        form = UserForm(data={"username": "testuser", "password": ""})
        self.assertEqual(form.errors["password"][0], REQUIRED_FIELD_ERROR)

    def test_positive_register_valid_data(self):
        form = UserForm(data={"username": "testuser", "password": "testpassword"})
        self.assertTrue(form.is_valid())

    def test_register_user_is_user_created(self):
        form = UserForm(data={"username": "testuser", "password": "testpassword"})
        user = form.save()
        self.assertIsInstance(user, User)

        users = User.objects.all()
        self.assertEqual(len(users), 1)

    def test_register_user_check_saved_user_fields(self):
        form = UserForm(data={"username": "testuser", "password": "testpassword"})
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))


class TestTodoForm(TestCase):
    def setUp(self) -> None:
        user = User(username="testuser")
        user.set_password("testpassword")
        user.save()

        self.user = user

    def test_negative_create_todo_empty_data_is_valid(self):
        form = TodoForm()
        self.assertFalse(form.is_valid())

    def test_negative_create_todo_empty_data_error_message(self):
        form = TodoForm(data={"title": "", "description": "", "user": None})
        self.assertEqual(form.errors["title"][0], REQUIRED_FIELD_ERROR)
        self.assertEqual(form.errors["description"][0], REQUIRED_FIELD_ERROR)
        self.assertEqual(form.errors["user"][0], REQUIRED_FIELD_ERROR)

    def test_negative_create_todo_empty_title_is_valid(self):
        form = TodoForm(data={"title": "", "description": "test", "user": self.user})
        self.assertFalse(form.is_valid())

    def test_negative_create_todo_empty_title_error_message(self):
        form = TodoForm(data={"title": "", "description": "test", "user": self.user})
        self.assertEqual(form.errors["title"][0], REQUIRED_FIELD_ERROR)
        self.assertFalse("description" in form.errors)
        self.assertFalse("user" in form.errors)

    def test_negative_create_todo_empty_description_is_valid(self):
        form = TodoForm(data={"title": "test", "description": "", "user": self.user})
        self.assertFalse(form.is_valid())

    def test_negative_create_todo_empty_description_error_message(self):
        form = TodoForm(data={"title": "test", "description": "", "user": self.user})
        self.assertEqual(form.errors["description"][0], REQUIRED_FIELD_ERROR)
        self.assertFalse("title" in form.errors)
        self.assertFalse("user" in form.errors)

    def test_negative_create_todo_empty_user_is_valid(self):
        form = TodoForm(data={"title": "test", "description": "test", "user": None})
        self.assertFalse(form.is_valid())

    def test_negative_create_todo_empty_user_error_message(self):
        form = TodoForm(data={"title": "test", "description": "test", "user": None})
        self.assertEqual(form.errors["user"][0], REQUIRED_FIELD_ERROR)
        self.assertFalse("title" in form.errors)
        self.assertFalse("description" in form.errors)

    def test_positive_create_todo(self):
        form = TodoForm(
            data={"title": "test", "description": "test", "user": self.user}
        )
        self.assertTrue(form.is_valid())

        return form.save()

    def test_create_todo_is_todo_created(self):
        todo = self.test_positive_create_todo()
        self.assertIsInstance(todo, Todo)

        todos = Todo.objects.all()
        self.assertEqual(len(todos), 1)

    def test_create_todo_check_saved_todo_fields(self):
        todo = self.test_positive_create_todo()
        self.assertEqual(todo.title, "test")
        self.assertEqual(todo.description, "test")
        self.assertFalse(todo.completed)
        self.assertEqual(todo.user, self.user)

    def test_update_todo(self):
        todo = self.test_positive_create_todo()

        form = TodoForm(
            data={
                "title": "test_updated",
                "description": "test_updated",
                "completed": True,
                "user": self.user,
            },
            instance=todo,
        )

        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(todo.title, "test_updated")
        self.assertEqual(todo.description, "test_updated")
        self.assertTrue(todo.completed)
