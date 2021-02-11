from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from users.models import User
from .forms import RecipeForm
from .help_functions import get_tag_filter
from .models import Ingredient, IngredientItem, Recipe


def index(request):
    # получаем фильтр по тегам
    custom_filter, tags = get_tag_filter(request)
    recipes = (Recipe.objects.filter(custom_filter).
               prefetch_related('ingredients').order_by('-pub_date'))
    # настраиваем paginator
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    # задаем контекст
    context = {'recipes': recipes, 'tags': tags, 'page': page,
               'paginator': paginator, 'url_name': 'index',
               'title': 'Рецепты'}
    return render(request, 'index.html', context)


def recipe_page(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.ingredients.all()
    return render(request, 'singlePage.html', {'recipe': recipe,
                                               'ingredients': ingredients,
                                               'url_name': 'recipe_page'})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None)
    context = {'form': form, 'url_name': 'new_recipe',
               'title': 'Создание рецепта'}
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
                name = name.replace("'", '"')
                obj = Ingredient.objects.get(title=name)
                item, flag = IngredientItem.objects.get_or_create(
                    ingredient=obj,
                    count=count)
                recipe.ingredients.add(item)
            return redirect('index')
        return render(request, 'formRecipe.html', context)
    return render(request, 'formRecipe.html', context)


@login_required
def recipe_edit(request, recipe_id):
    article = get_object_or_404(Recipe, id=recipe_id)
    if article.author != request.user:
        return redirect('index')
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=article)
    ing_list = article.ingredients.select_related('ingredient')
    tags = article.tags
    context = {'form': form, 'url_name': 'recipe_edit',
               'title': 'Редактирование рецепта', 'ing_list': ing_list,
               'tags': tags, 'recipe_id': recipe_id}
    if request.method == 'POST':
        if form.is_valid():
            name_ing_list = request.POST.getlist('nameIngredient')
            if not name_ing_list:
                return render(request, 'recipeEditForm.html', context)
            count_ing_list = request.POST.getlist('valueIngredient')
            dimension_ing_list = request.POST.getlist('unitsIngredient')
            form.save()
            article.ingredients.clear()
            for name, count, dimension in zip(name_ing_list, count_ing_list,
                                              dimension_ing_list):
                obj = Ingredient.objects.get(title=name)
                item, flag = IngredientItem.objects.get_or_create(
                    ingredient=obj,
                    count=count.replace(',', '.'))
                article.ingredients.add(item)
            return redirect('recipe_page', recipe_id)
        return render(request, 'recipeEditForm.html', context)
    return render(request, 'recipeEditForm.html', context)


@login_required
def recipe_delete(request, recipe_id):
    article = get_object_or_404(Recipe, id=recipe_id)
    if article.author != request.user:
        return redirect('index')
    article.delete()
    return redirect('index')


@login_required
def favorites(request):
    user = get_object_or_404(User, username=request.user)
    custom_filter, tags = get_tag_filter(request)
    custom_filter &= Q(fans__user=user)
    # получаем записи
    recipes = (Recipe.objects.filter(custom_filter).
               prefetch_related('ingredients').order_by('-pub_date'))
    # настраиваем paginator
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    # задаем контекст
    context = {'recipes': recipes, 'tags': tags, 'page': page,
               'paginator': paginator, 'url_name': 'favorites',
               'title': 'Избранное'}
    return render(request, 'index.html', context)


def profile(request, author_id):
    author = get_object_or_404(User, id=author_id)
    custom_filter, tags = get_tag_filter(request)
    recipes = (author.recipes.filter(custom_filter).
               order_by('-pub_date'))
    # настраиваем paginator
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    # задаем контекст
    context = {'recipes': recipes, 'tags': tags, 'page': page,
               'paginator': paginator, 'url_name': 'profile',
               'title': author.get_full_name, "author": author}
    return render(request, 'index.html', context)


@login_required
def subscribes_view(request):
    user = get_object_or_404(User, username=request.user)
    cards = (user.subscribes.prefetch_related('author__recipes').
             order_by('author__first_name'))
    paginator = Paginator(cards, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {'page': page, 'tags': [],
               'paginator': paginator, 'url_name': 'subscribes',
               'title': 'Мои подписки'}
    return render(request, 'subscribe.html', context)


@login_required
def shop_list_view(request):
    user = get_object_or_404(User, username=request.user)
    shoplist = user.shop_list.select_related('recipe')
    context = {'title': 'Список покупок', 'url_name': 'shop_list',
               'shoplist': shoplist}
    return render(request, 'shopList.html', context)


@login_required
def generate_pdf_view(request):
    user = get_object_or_404(User, username=request.user)
    ing_dict = {}
    shop_list = user.shop_list.select_related('recipe')
    for el in shop_list:
        ingredients = el.recipe.ingredients.select_related('ingredient')
        for ingredient in ingredients:
            name = ingredient.ingredient.title
            count = ingredient.count
            dimension = ingredient.ingredient.dimension
            if name not in ing_dict:
                ing_dict[name] = [count, dimension]
            else:
                ing_dict[name][0] += count
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shopList.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    p.setFont('Arial', 20)
    x = 50
    y = 750
    for num, el in enumerate(ing_dict):
        if y <= 100:
            y = 700
            p.showPage()
            p.setFont('Arial', 20)
        p.drawString(x, y,
                     f'№{num + 1}: {el} - {ing_dict[el][0]} {ing_dict[el][1]}')
        y -= 30
    p.showPage()
    p.save()
    return response
