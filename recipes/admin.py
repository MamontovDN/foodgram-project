from django.contrib import admin

# from django.db.models import Q
from django_admin_multiple_choice_list_filter.list_filters import (
    MultipleChoiceListFilter,
)

from .models import (
    Recipe,
    Ingredient,
    Favorites,
    Subscribe,
    ShopListItem,
    IngredientItem,
    TAGS,
)


class IngredientItemInline(admin.TabularInline):
    model = Recipe.ingredients.through


"""
Фильтр для тегов, так как в multiselectedfield
нет поддержки стандартного list_filter
"""


class TagFilter(MultipleChoiceListFilter):
    title = "Теги"
    parameter_name = "tags"

    def lookups(self, request, model_admin):
        return TAGS

    #
    # def queryset(self, request, queryset):
    #     if not self.value():
    #         return queryset
    #     if self.value() == "breakfast":
    #         return queryset.filter(Q(tags__contains="breakfast"))
    #     elif self.value() == "dinner":
    #         return queryset.filter(Q(tags__contains="dinner"))
    #     elif self.value() == "supper":
    #         return queryset.filter(Q(tags__contains="supper"))


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientItemInline,)
    list_display = ("pk", "title", "author", "tags")
    search_fields = ("title",)
    list_filter = (
        "author",
        "title",
        TagFilter,
    )
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
