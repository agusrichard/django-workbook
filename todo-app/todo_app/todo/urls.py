from django.urls import path

from .views import CreateTodoView

urlpatterns = [
    path('', CreateTodoView.as_view(), name='todo-view')
]