from django.contrib import admin

from .models import Recipe, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    filter_vertical = ('ingredients',)
    list_display = ("pk", "title", "author",)
    search_fields = ("title",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "dimension",)
    search_fields = ("title",)
    list_filter = ("dimension",)
    empty_value_display = "-пусто-"


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
