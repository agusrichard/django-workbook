from django.http import Http404
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Restaurant, Product
from .serializers import RestaurantSerializer, ProductSerializer

# @api_view(['GET', 'POST'])
# def restaurants_list(request, format=None):
#     if request.method == 'GET':
#         restaurants = Restaurant.objects.all()
#         serializer = RestaurantSerializer(restaurants, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = RestaurantSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RestaurantList(APIView):
#     def get(self, request, format=None):
#         restaurants = Restaurant.objects.all()
#         serializer = RestaurantSerializer(restaurants, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = RestaurantSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RestaurantList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# @api_view(['GET', 'PUT', 'DELETE'])
# def restaurant_detail(request, pk, format=None):
#     try:
#         restaurant = Restaurant.objects.get(pk=pk)
#     except Restaurant.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = RestaurantSerializer(restaurant)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = RestaurantSerializer(restaurant, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         restaurant.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class RestaurantDetail(APIView):
#     def get_object(self, pk):
#         try:
#             restaurant = Restaurant.objects.get(pk=pk)
#             return restaurant
#         except Restaurant.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         restaurant = self.get_object(pk=pk)
#         serializer= RestaurantSerializer(restaurant)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         restaurant = self.get_object(pk=pk)
#         print(restaurant)
#         serializer = RestaurantSerializer(restaurant, request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         restaurant = self.get_object(pk=pk)
#         restaurant.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class RestaurantDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer

#     def get(self, request, pk, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, pk, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, pk, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer