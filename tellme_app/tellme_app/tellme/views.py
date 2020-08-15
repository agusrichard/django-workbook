from django.http import HttpResponse
from django.shortcuts import render
from .models import User

# Create your views here.
def index(request):
    users = User.objects.all()
    return render(request, 'tellme/index.html', { 'users': users })

def user(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'tellme/user.html', { 'user': user })