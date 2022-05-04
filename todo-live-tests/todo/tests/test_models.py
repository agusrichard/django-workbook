from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from ..models import Todo


class TestTodoModel(TestCase):
    def setUp(self) -> None:
        user = User(username="testuser")
        user.set_password("testpassword")
        user.save()

        self.user = user

    def test_negative_title_unspecified(self):
        todo = Todo()
        with self.assertRaises(IntegrityError):
            todo.save()

    def test_negative_description_unspecified(self):
        todo = Todo(title="test")
        with self.assertRaises(IntegrityError):
            todo.save()

    def test_negative_user_unspecified(self):
        todo = Todo(title="test", description="test")
        with self.assertRaises(IntegrityError):
            todo.save()

    def test_positive_create_todo(self):
        todo = Todo(title="test", description="test", user=self.user)
        todo.save()

        self.assertEqual(todo.title, "test")
        self.assertEqual(todo.description, "test")
        self.assertEqual(todo.user, self.user)

        return todo

    def test_positive_update_todo(self):
        todo = self.test_positive_create_todo()

        todo.title = "test2"
        todo.description = "test2"
        todo.save()

        self.assertEqual(todo.title, "test2")
        self.assertEqual(todo.description, "test2")
        self.assertEqual(todo.user, self.user)

    def test_todo_str(self):
        todo = self.test_positive_create_todo()

        self.assertEqual(str(todo), "test")
