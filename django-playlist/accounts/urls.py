from django.urls import path

from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('register/', views.doing_post, name='doing_post')
]