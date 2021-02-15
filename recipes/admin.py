from django.contrib import admin

from .models import (
    Recipe,
    Ingredient,
    Favorites,
    Subscribe,
    ShopListItem,
    IngredientItem,
)


class IngredientItemInline(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeAdmin(admin.ModelAdmin):
    # filter_vertical = ("ingredients",)
    inlines = (IngredientItemInline,)
    list_display = ("pk", "title", "author", "tags")
    search_fields = ("title",)
    list_filter = ("author", "title", "tags",)
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "dimension",
    )
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user",)
    empty_value_display = "-пусто-"


class SubscribeAdmins(admin.ModelAdmin):
    list_display = ("author", "user")
    list_filter = ("user", "author")
    empty_value_display = "-пусто-"


class ShopListAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user",)
    search_fields = ("recipe",)


class IngredientItemAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "count")
    list_filter = ("ingredient",)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Subscribe, SubscribeAdmins)
admin.site.register(ShopListItem, ShopListAdmin)
admin.site.register(IngredientItem, IngredientItemAdmin)
