from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
]
