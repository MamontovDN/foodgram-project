from django.core.validators import MinValueValidator
from django.db import models

from users.models import User
from multiselectfield import MultiSelectField

TAGS = (("breakfast", "Завтрак"), ("dinner", "Обед"), ("supper", "Ужин"))


class Ingredient(models.Model):
    """модель Ингредиента"""

    title = models.CharField(max_length=100, verbose_name="название")
    dimension = models.CharField(
        max_length=50,
        verbose_name="единица измерения",
        default="г.",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.title} - ...{self.dimension}"


class Recipe(models.Model):
    """модель Рецепта"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(max_length=100)
    ingredients = models.ManyToManyField("IngredientItem")
    img = models.ImageField(upload_to="recipes/", blank=True, null=True)
    description = models.TextField()
    tags = MultiSelectField(max_choices=3, choices=TAGS)
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="дата публикации"
    )
    duration = models.PositiveSmallIntegerField(
        "время приготовления", validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.title} by {self.author} "


class IngredientItem(models.Model):
    """Модель Ингредиента с кол-вом для модели Рецепта"""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.DecimalField(
        verbose_name="кол-во", max_digits=6, decimal_places=1
    )

    class Meta:
        verbose_name = "Ингредиент из рецепта"
        verbose_name_plural = "Ингредиенты из рецептов"

    def __str__(self):
        return (
            f"{self.ingredient.title} - {self.count} "
            f"{self.ingredient.dimension}"
        )


class Favorites(models.Model):
    """модель Избранного"""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="fans"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"


class Subscribe(models.Model):
    """модель Подписки"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribers"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribes"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class ShopListItem(models.Model):
    """модель Списка покупок"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shop_list"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="to_buy"
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
