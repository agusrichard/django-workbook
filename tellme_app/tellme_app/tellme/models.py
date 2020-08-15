from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name='email address')
    password = models.CharField(blank=False, max_length=128, verbose_name='password')
    full_name = models.CharField(blank=True, max_length=150, verbose_name='full name')

    def __str__(self):
        return f"<User: {self.username}, {self.email}>"

    def __repr__(self):
        return self.__str__()

class Tell(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

