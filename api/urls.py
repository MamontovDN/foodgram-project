from django.urls import path

from . import views

urlpatterns = [
    path('ingredients/', views.IngredientViewSet.as_view(),
         name='api_ingredient'),
]
