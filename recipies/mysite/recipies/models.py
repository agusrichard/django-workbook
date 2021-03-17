from django.db import models

class DateTimeInfo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['created_date']

class Restaurant(DateTimeInfo):
    name = models.CharField(max_length=64)
    address = models.TextField()

class ProductType(models.IntegerChoices):
    FOOD = 1
    BEVERAGES = 2
    OTHERS = 3

class Product(DateTimeInfo):

    product_type = models.IntegerField(choices=ProductType.choices)
    name = models.CharField(max_length=128)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

