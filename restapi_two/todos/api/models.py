from django.db import models
from django.contrib.auth.models import User 

class Todo(models.Model):
    created = models.DateField()
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.content
