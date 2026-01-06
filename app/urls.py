from django.contrib import admin
from django.urls import path, include
from .views import CarDetailApiView, read_create, create, update, delete

urlpatterns = [
    path('car/', CarDetailApiView.as_view()),
    path('car/<int:car_id>/', CarDetailApiView.as_view()),
    path('car-fbv-read/', read_create),
    path('car-fbv-create/', create),
    path('car-fbv-update/<int:car_id>/', update),
    path('car-fbv-delete/<int:car_id>/', delete),
]
