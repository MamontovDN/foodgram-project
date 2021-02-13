from django.shortcuts import get_object_or_404
from registration.forms import User
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    IngredientSerializer,
    FavoritesSerializer,
    SubscribeSerializer,
    ShopListItemSerializer,
)
from recipes.models import Ingredient, Favorites, Subscribe, ShopListItem


"""
класс родитель с переопределенным мнтодом DELETE для Subscribe, Favorite и
Purchase
"""


class Mix(generics.CreateAPIView, generics.DestroyAPIView):
    api_name = ""

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user)
        if self.api_name == "favorite":
            obj = user.favorites.filter(recipe__id=kwargs["id"])
        elif self.api_name == "subscribe":
            obj = user.subscribes.filter(author__id=kwargs["id"])
        else:
            obj = user.shop_list.filter(recipe__id=kwargs["id"])
        if obj.delete():
            return Response({"Success": True})
        return Response({"Success": False})


class IngredientViewSet(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^title"]


class FavoritesView(Mix):
    serializer_class = FavoritesSerializer
    queryset = Favorites.objects.all()
    permission_classes = [IsAuthenticated]
    api_name = "favorite"


class SubscribeView(Mix):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subscribe.objects.all()
    api_name = "subscribe"


class ShopListView(Mix):
    queryset = ShopListItem.objects.all()
    serializer_class = ShopListItemSerializer
    permission_classes = [IsAuthenticated]
    api_name = "purchase"
