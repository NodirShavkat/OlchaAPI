from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Car
from .serializers import CarSerializer
from rest_framework import status
from rest_framework.decorators import api_view


# CBV da Car modeli uchun CRUD
class CarDetailApiView(APIView):
    # read
    def get(self, request, car_id=None):
        if car_id:
            car = Car.objects.get(id=car_id)
            serializer = CarSerializer(car)
        else:
            cars = Car.objects.all()
            serializer = CarSerializer(cars, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create
    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update    
    def put(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete
    def delete(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)	
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# FBV da Car modeli uchun CRUD
@api_view(['GET', 'POST'])
def read_create(request):
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create(request):
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def update(request, car_id):
    if request.method == 'GET':
        car = Car.objects.get(id=car_id)
        serializer = CarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        car = get_object_or_404(Car, id=car_id)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete(request, car_id):
        car = get_object_or_404(Car, id=car_id)	
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
