from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantList.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),
    path('user/', views.UserList.as_view(), name='user_list'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)