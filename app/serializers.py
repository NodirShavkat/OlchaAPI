from rest_framework import serializers
from .models import Category, Product

class ParentCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ()

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)

class UpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id",'title','slug','image', 'parent', 'is_active']

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('id', 'created_at')

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ()
