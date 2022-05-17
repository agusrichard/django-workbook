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

    def test_positive_create_todo(self):
        todo = Todo(title="test", description="test", user=self.user)
        todo.save()

        self.assertEqual(todo.title, "test")
        self.assertEqual(todo.description, "test")
        self.assertFalse(todo.completed)
        self.assertIsNotNone(todo.created_at)
        self.assertEqual(todo.user, self.user)

        return todo

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

    def test_positive_update_todo(self):
        todo = self.test_positive_create_todo()

        todo.title = "test2"
        todo.description = "test2"
        todo.save()

        self.assertEqual(todo.title, "test2")
        self.assertEqual(todo.description, "test2")
        self.assertFalse(todo.completed)
        self.assertIsNotNone(todo.created_at)
        self.assertEqual(todo.user, self.user)

    def test_negative_update_todo_title_to_null(self):
        todo = self.test_positive_create_todo()

        todo.title = None
        with self.assertRaises(IntegrityError):
            todo.save()

    def test_negative_update_todo_description_to_null(self):
        todo = self.test_positive_create_todo()

        todo.description = None
        with self.assertRaises(IntegrityError):
            todo.save()

    def test_negative_update_todo_user_to_null(self):
        todo = self.test_positive_create_todo()

        todo.user = None
        with self.assertRaises(IntegrityError):
            todo.save()

    def test_positive_get_todo_by_id(self):
        todo = self.test_positive_create_todo()

        todo_get = Todo.objects.get(id=todo.id)

        self.assertEqual(todo_get.title, "test")
        self.assertEqual(todo_get.description, "test")
        self.assertFalse(todo.completed)
        self.assertIsNotNone(todo_get.created_at)
        self.assertEqual(todo_get.user, self.user)

    def test_negative_get_todo_by_id_not_found(self):
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=1)

    def test_positive_get_all_todos(self):
        for i in range(10):
            todo = Todo(title=f"test-{i}", description=f"test-{i}", user=self.user)
            todo.save()

        todos = Todo.objects.all()
        self.assertEqual(len(todos), 10)

    def test_positive_delete_todo(self):
        todo = self.test_positive_create_todo()

        todo.delete()

        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=todo.id)

    def test_todo_str(self):
        todo = self.test_positive_create_todo()

        self.assertEqual(str(todo), "test")
