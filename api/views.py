from django.shortcuts import render
from rest_framework import mixins, viewsets, filters, generics

from .permissions import AdminPermission, ReadOnlyPermission
from .serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientViewSet(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^title"]
