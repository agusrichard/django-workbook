from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello_world(request, format=None):
    return Response('Hello')

@api_view(['POST'])
def doing_post(request, format=None):
    print('doing post request', request.data)
    return Response('Hello')