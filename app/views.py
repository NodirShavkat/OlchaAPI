from django.shortcuts import render, get_object_or_404
from .models import Car, Category, Product
from .serializers import ParentCategoryModelSerializer, CreateCategorySerializer, CreateProductSerializer, ProductListSerializer
from .permissions import UpdateWithinHoursPermission

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class ParentCategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ParentCategoryModelSerializer

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull = True)
        return queryset    
    

class ChildrenCategoryByCategorySlug(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ParentCategoryModelSerializer

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        queryset = Category.objects.filter(slug=category_slug).first()
        if not queryset:
            return Category.objects.none()
        return queryset.children.all()
    

class ProductListByChildCategorySlug(ListAPIView):
    pass 
    

class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CreateCategorySerializer()


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


# class CarDetailView(RetrieveUpdateAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
#     permission_classes = [UpdateWithinHoursPermission]


# # CBV da Car modeli uchun CRUD
# class CarDetailApiView(APIView):
#     # read
#     def get(self, request, car_id=None):
#         queryset = Car.objects.all()

#         if car_id:
#             car = get_object_or_404(Car, id=car_id)
#             serializer = CarSerializer(car, many=False)
#             return Response(serializer.data)

#         q_id = request.GET.get('id')
#         color = request.GET.get('color')
#         price = request.GET.get('price')

#         if q_id:
#             queryset = queryset.filter(id=q_id)

#         if color:
#             queryset = queryset.filter(color=color)

#         if price:
#             queryset = queryset.filter(price=price)
        
#         serializer = CarSerializer(queryset, many=True)
#         return Response(serializer.data)
#     # old version
#     # def get(self, request, car_id=None):
#     #     if car_id:
#     #         car = Car.objects.get(id=car_id)
#     #         serializer = CarSerializer(car)
#     #         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     #     query_id = request.GET.get('id', None)
#     #     if query_id:
#     #         car = Car.objects.get(id=query_id)
#     #         serializer = CarSerializer(car)
#     #         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     #     cars = Car.objects.all()
#     #     serializer = CarSerializer(cars, many=True)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)

#     # create
#     def post(self, request):
#         serializer = CarSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # update    
#     def put(self, request, car_id):
#         car = get_object_or_404(Car, id=car_id)
#         serializer = CarSerializer(car, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # delete
#     def delete(self, request, car_id):
#         car = get_object_or_404(Car, id=car_id)	
#         car.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # FBV da Car modeli uchun CRUD
# @api_view(['GET', 'POST'])
# def read_create(request):
#     if request.method == 'POST':
#         serializer = CarSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     cars = Car.objects.all()
#     serializer = CarSerializer(cars, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def create(request):
#     if request.method == 'POST':
#         serializer = CarSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT'])
# def update(request, car_id):
#     if request.method == 'GET':
#         car = Car.objects.get(id=car_id)
#         serializer = CarSerializer(car)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == 'PUT':
#         car = get_object_or_404(Car, id=car_id)
#         serializer = CarSerializer(car, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def delete(request, car_id):
#         car = get_object_or_404(Car, id=car_id)	
#         car.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'created_at': user.created_at
        })


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Logged out"})
    