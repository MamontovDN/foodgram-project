from django.conf import settings
from django.conf.urls import handler404  # noqa
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

handler404 = 'recipes.views.page_not_found'  # noqa

urlpatterns = [
    path('api/', include('api.urls')),
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
