from rest_framework import serializers
from .models import Car

# class CarSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=20)
#     color = serializers.CharField(max_length=20)
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'color', 'price']
