import io
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from .models import Todo
from .serializers import TodoSerializer


class CreateTodoView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            print('data', request.data.get('title'))
            todo = Todo(title=request.data.get('title'), description=request.data.get('description'), author=request.user)
            todo.save()
            return Response({
                'data': TodoSerializer(todo).data
            })
        except Exception as error:
            print('error', error)
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        try:
            todos = Todo.objects.filter(author=request.user)
            print('todos', todos)
            return Response({
                'data': TodoSerializer(todos, many=True).data
            })
        except Exception as error:
            print('error', error)
            return Response(status=status.HTTP_400_BAD_REQUEST)