from django.db import models
from django.contrib.auth.models import User

class DateTimeInfo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['created_date']

class Restaurant(DateTimeInfo):
    name = models.CharField(max_length=64)
    address = models.TextField()
    owner = models.ForeignKey(User, related_name='restaurants', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ProductType(models.IntegerChoices):
    FOOD = 1
    BEVERAGES = 2
    OTHERS = 3

class Product(DateTimeInfo):
    product_type = models.IntegerField(choices=ProductType.choices)
    name = models.CharField(max_length=128)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

