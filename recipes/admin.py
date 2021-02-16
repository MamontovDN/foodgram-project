from django.contrib import admin

from django.db.models import Q
from django_admin_multiple_choice_list_filter.list_filters import (
    MultipleChoiceListFilter,
)

from .models import (
    Recipe,
    Ingredient,
    Favorites,
    Subscribe,
    ShopListItem,
    TAGS,
)


class IngredientItemInline(admin.TabularInline):
    model = Recipe.ingredients.through


"""
Фильтр для тегов, с множественным выбором
"""


class TagFilter(MultipleChoiceListFilter):
    title = "Теги"
    parameter_name = "tags"

    def lookups(self, request, model_admin):
        return TAGS

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        tags = self.value().split(",")
        tag_filter = Q(tags__contains=tags[0])
        for tag in tags[1:]:
            tag_filter |= Q(tags__contains=tag)
        return queryset.filter(tag_filter)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientItemInline,)
    fields = ("__all__", "get_favorite")
    list_display = ("pk", "title", "author", "tags")
    search_fields = ("title",)
    list_filter = (
        "author",
        "title",
        TagFilter,
    )
    empty_value_display = "-пусто-"

    def get_favorite(self, obj):
        return obj.fans.count()

    get_favorite.short_description = "В избранном"


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


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Subscribe, SubscribeAdmins)
admin.site.register(ShopListItem, ShopListAdmin)
