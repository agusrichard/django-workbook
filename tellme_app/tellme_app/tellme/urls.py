from django.urls import path
from . import views

app_name = 'tellme'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.user, name='user')
]