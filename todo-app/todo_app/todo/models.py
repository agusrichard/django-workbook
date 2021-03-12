from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)