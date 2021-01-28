from django.db import models

from users.models import User
from multiselectfield import MultiSelectField

TAGS = (('breakfast', 'Завтрак'),
        ('dinner', 'Обед'),
        ('supper', 'Ужин'))


class Ingredient(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    dimension = models.CharField(max_length=50,
                                 verbose_name='единица измерения',
                                 default='г.',
                                 blank=True, null=True)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f'{self.title} - ...{self.dimension}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(max_length=100)
    ingredients = models.ManyToManyField('IngredientItem')
    img = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField()
    tags = MultiSelectField(max_choices=3, choices=TAGS)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='дата публикации')
    duration = models.PositiveSmallIntegerField('время приготовления')

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f'{self.title} by {self.author} '


class IngredientItem(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='кол-во')

    def __str__(self):
        return (
            f'{self.ingredient.title} - {self.count} '
            f'{self.ingredient.dimension}'
        )
