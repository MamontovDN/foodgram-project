from django.db.models import Q

from recipes.models import Ingredient, IngredientItem


def get_tag_filter(request):
    # получаем информацию по выбраным тегам
    tags = request.GET.get('tags', 'breakfast,dinner,supper')
    tags = tags.split(',')
    # случай когда не выбран ни один тег
    if tags == ['']:
        tags = ['None']
    # генерируем фильтр по тегам
    tag_filter = Q(tags__contains=tags[0])
    for tag in tags[1:]:
        tag_filter |= Q(tags__contains=tag)
    return tag_filter, tags


def get_ing_list(name_list, count_list):
    ing_list = []
    for name, count in zip(name_list, count_list,):
        # обрабатываем случай если в названии ингредиента есть кавычки
        # которые в formRecipe.js были заменены на апострофы
        name = name.replace("'", '"')
        obj = Ingredient.objects.get(title=name)
        # изменяем десятичный разделитель
        count = count.replace(',', '.')
        item, flag = IngredientItem.objects.get_or_create(
            ingredient=obj,
            count=count)
        ing_list.append(item)
    return ing_list
