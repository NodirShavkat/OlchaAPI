from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('', views.ParentCategoryListAPIView.as_view()),
    path('category/<slug:slug>/', views.ChildrenCategoryByCategorySlug.as_view()),
    path('category/create', views.CategoryCreateAPIView.as_view()),
    path('category/update/<int:category_id>/', views.CategoryUpdateAPIView.as_view(), name='category-update'),
    path('create/product', views.ProductCreateAPIView.as_view()),
    path('products', views.ProductListAPIView.as_view()),

    # Car urls:
    # path('car/', views.CarDetailApiView.as_view()),
    # path('car/<int:car_id>/', views.CarDetailApiView.as_view()),
    # path('car-fbv-read/', views.read_create),
    # path('car-fbv-create/', views.create),
    # path('car-fbv-update/<int:car_id>/', views.update),
    # path('car-fbv-delete/<int:car_id>/', views.delete),

    # Auth
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
]
