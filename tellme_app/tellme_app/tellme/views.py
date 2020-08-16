from django.http import HttpResponse
from django.shortcuts import render
from .models import User

# Create your views here.
def home(request):
    return render(request, 'tellme/pages/home.html')

def register(request):
    return render(request, 'tellme/pages/register.html')

def login(request):
    return render(request, 'tellme/pages/login.html')