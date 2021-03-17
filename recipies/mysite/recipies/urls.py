from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.RestaurantList.as_view(), name='restaurants_list'),
    path('<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)