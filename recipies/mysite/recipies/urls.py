from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.restaurants_list, name='restaurants_list'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)