from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import RecipeForm
from .models import Ingredient, IngredientItem, Recipe


def index(request):
    # получаем информацию по выбраным тегам
    tags = request.GET.get('tags', 'breakfast,dinner,supper')
    print(tags)
    tags = tags.split(',')
    # случай когда не выбран ни один тег
    if tags == ['']:
        tags = ['None']
    # генерируем фильтр по тегам
    tag_filter = Q(tags__contains=tags[0])
    for tag in tags[1:]:
        tag_filter |= Q(tags__contains=tag)
    # получаем записи
    recipes = (Recipe.objects.filter(tag_filter).
               prefetch_related('ingredients').order_by('-pub_date'))
    # настраиваем paginator
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    print(page.has_other_pages())
    # задаем контекст
    context = {'recipes': recipes, 'tags': tags, 'page': page,
               'paginator': paginator, 'url_name': 'index'}
    return render(request, 'index.html', context)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            name_ing_list = request.POST.getlist('nameIngredient')
            if not name_ing_list:
                return render(request, 'formRecipe.html', context)
            count_ing_list = request.POST.getlist('valueIngredient')
            dimension_ing_list = request.POST.getlist('unitsIngredient')
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            pk = recipe.pk
            recipe = Recipe.objects.get(pk=pk)
            for name, count, dimension in zip(name_ing_list, count_ing_list,
                                              dimension_ing_list):
                obj = Ingredient.objects.get(title=name)
                item, flag = IngredientItem.objects.get_or_create(
                    ingredient=obj,
                    count=count)
                recipe.ingredients.add(item)
                print(recipe.ingredients)
            return redirect('index')
        return render(request, 'formRecipe.html', context)
    return render(request, 'formRecipe.html', context)
