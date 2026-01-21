from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/token/', obtain_auth_token),
    # path('api/token/'),
    path('apelsin.uz/', include('app.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
