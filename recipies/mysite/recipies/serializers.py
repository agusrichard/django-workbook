from rest_framework import serializers

from .models import Restaurant, ProductType, Product

# class RestaurantSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=64)
#     address = serializers.CharField()
#     created_date = serializers.DateTimeField(read_only=True)
#     updated_date = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         """
#             Create and return a new `Restaurant` instance, given the validated data.
#         """
#         return Restaurant.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#             Update and return an existing `Restaurant` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name')
#         instance.address = validated_data.get('address')
#         instance.save()
#         return instance

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=128)
#     restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
#     product_type = serializers.ChoiceField(choices=ProductType.choices)
#     created_date = serializers.DateTimeField(read_only=True)
#     updated_date = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         """
#             Create and return a new `Product` instance, given the validated data.
#         """
#         return Product.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#             Update and return an existing `Product` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name')
#         instance.restaurant = validated_data.get('restaurant')
#         instance.product_type = validated_data.get('product_type')
#         instance.save()
#         return instance

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'created_date', 'updated_date']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'restaurant', 'product_type', 'created_date', 'updated_date']