from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import (
    Ingredient,
    Favorites,
    Recipe,
    Subscribe,
    ShopListItem,
)

from users.models import User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Ingredient


class FavoritesSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source="recipe", slug_field="id", queryset=Recipe.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ["id", "user"]
        model = Favorites


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source="author", slug_field="id", queryset=User.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ["id", "user"]
        model = Subscribe

    def validate(self, attrs):
        if attrs['author'] == attrs['user']:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return super().validate(attrs)


class ShopListItemSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source="recipe", slug_field="id", queryset=Recipe.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ["id", "user"]
        model = ShopListItem
