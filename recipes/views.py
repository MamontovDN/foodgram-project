from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView

from .forms import RecipeForm
from .models import Ingredient, IngredientItem, Recipe


def index(request):
    return render(request, 'index.html')


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None)
    print(Recipe.objects.last().ingredients.all())
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            name_ing_list = request.POST.getlist('nameIngredient')
            if not name_ing_list:
                return render(request, 'formRecipe.html', context)
            count_ing_list = request.POST.getlist('valueIngredient')
            dimension_ing_list = request.POST.getlist('unitsIngredient')
            tags = form.cleaned_data.get("tags")
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
