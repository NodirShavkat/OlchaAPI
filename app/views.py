from .models import Category, Product
from app import serializers
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class ParentCategoryListAPIView(APIView):
    def get(self, request):
        cache_key = 'parent_category_list'
        data = cache.get(cache_key)

        if data is None:
            queryset = Category.objects.filter(parent__isnull=True)
            serializer = serializers.ParentCategoryModelSerializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60*5) 
        
        return Response(data)

class ChildrenCategoryByCategorySlug(APIView):
    def get(self, request, slug):
        cache_key = f'children_category_{slug}'
        data = cache.get(cache_key)

        if data is None:
            category = Category.objects.filter(slug=slug).first()
            if not category:
                return Response([], status=200)
            
            queryset = category.children.all()
            serializer = serializers.ParentCategoryModelSerializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60*5)

        return Response(data)

    # queryset = Category.objects.all()
    # serializer_class = serializers.ParentCategoryModelSerializer

    # def get_queryset(self):
    #     category_slug = self.kwargs['slug']
    #     queryset = Category.objects.filter(slug=category_slug).first()
    #     if not queryset:
    #         return Category.objects.none()
    #     return queryset.children.all()
    

class ProductListByChildCategorySlug(ListAPIView):
    pass 
    

class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CreateCategorySerializer()

# Update Category
class CategoryUpdateAPIView(APIView):
    def put(self, request, category_id=None):
        category = get_object_or_404(Category, id=category_id)

        serializer = serializers.UpdateCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"not valid", "details": serializer.errors})
        
    def patch(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)

        serializer = serializers.UpdateCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.CreateProductSerializer


class ProductListAPIView(ListAPIView):
    def get(self, request):
        cache_key = 'product_list'
        data = cache.get(cache_key)

        if data is None:
            queryset = Product.objects.all()
            serializer = serializers.ProductListSerializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60*5)

        return Response(data)

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
