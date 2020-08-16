from django.urls import path
from . import views

app_name = 'tellme'
urlpatterns = [
    path('', views.home, name='home'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login')
]