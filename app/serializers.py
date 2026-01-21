from rest_framework import serializers
from .models import Car, Category, Product

class ParentCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ()

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('id', 'created_at')

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ()
