import reportlab
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.settings import OBJ_ON_PAGE
from users.models import User
from .forms import RecipeForm
from .help_functions import get_tag_filter, get_ing_list
from .models import Recipe


def index(request):
    # получаем фильтр по тегам
    custom_filter, tags = get_tag_filter(request)
    recipes = (
        Recipe.objects.filter(custom_filter)
        .prefetch_related("ingredients")
        .order_by("-pub_date")
    )
    # настраиваем paginator
    paginator = Paginator(recipes, OBJ_ON_PAGE)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)
    # задаем контекст
    context = {
        "recipes": recipes,
        "tags": tags,
        "page": page,
        "paginator": paginator,
        "url_name": "index",
        "title": "Рецепты",
    }
    return render(request, "index.html", context)


def recipe_page(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.ingredients.select_related("ingredient")
    favorite_count = recipe.fans.count()
    context = {
        "recipe": recipe,
        "ingredients": ingredients,
        "url_name": "recipe_page",
        "favorite_count": favorite_count,
    }
    return render(request, "singlePage.html", context)


@login_required
def new_recipe(request, **kwargs):
    # Задаем стандартные пустые значения если это создание рецепта
    article = None
    tags = []
    ing_list = []
    title = "Создание рецепта"
    url_name = "new_recipe"
    recipe_id = kwargs.get("recipe_id")
    # обрабатываем случай если это редактирование рецепта
    if recipe_id:
        article = get_object_or_404(Recipe, id=recipe_id)
        if article.author != request.user:
            return redirect("index")
        ing_list = article.ingredients.select_related("ingredient")
        tags = article.tags
        title = "Редактирование рецепта"
        url_name = "recipe_edit"
    # создаем форму и контекст
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=article
    )
    context = {
        "form": form,
        "url_name": url_name,
        "title": title,
        "tags": tags,
        "ing_list": ing_list,
        "ing_error": False,
        "recipe_id": recipe_id,
    }
    if request.method == "POST":
        # получаем введенные ингредиетны
        name_ing_list = request.POST.getlist("nameIngredient")
        # если их нет возвращаемся к созданию формы с ошибкой
        if not name_ing_list:
            context["ing_error"] = True
            return render(request, "formRecipe.html", context)
        # получаем кол-во ингредиентов
        count_ing_list = request.POST.getlist("valueIngredient")
        # создаем список объектов IngredientItem для добавления в рецепт
        # либо отправки их в форму в при ошибке валидности
        ing_list = get_ing_list(name_ing_list, count_ing_list)
        context["ing_list"] = ing_list
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe.ingredients.clear()
            # добавляем список ингредиентов в рецепт
            for item in ing_list:
                recipe.ingredients.add(item)
            return redirect("recipe_page", recipe.id)
        return render(request, "formRecipe.html", context)
    return render(request, "formRecipe.html", context)


@login_required
def recipe_delete(request, recipe_id):
    article = get_object_or_404(Recipe, id=recipe_id)
    if article.author != request.user:
        return redirect("index")
    article.delete()
    return redirect("index")


@login_required
def favorites(request):
    user = get_object_or_404(User, username=request.user)
    # создаем фильтр для тегов
    custom_filter, tags = get_tag_filter(request)
    # добавляем фильтр для выбора только избранных для юзера рецептов
    custom_filter &= Q(fans__user=user)
    # получаем записи
    recipes = (
        Recipe.objects.filter(custom_filter)
        .prefetch_related("ingredients")
        .order_by("-pub_date")
    )
    # настраиваем paginator
    paginator = Paginator(recipes, OBJ_ON_PAGE)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)
    # задаем контекст
    context = {
        "recipes": recipes,
        "tags": tags,
        "page": page,
        "paginator": paginator,
        "url_name": "favorites",
        "title": "Избранное",
    }
    return render(request, "index.html", context)


def profile(request, author_id):
    author = get_object_or_404(User, id=author_id)
    # создаем фильтр для тегов
    custom_filter, tags = get_tag_filter(request)
    recipes = author.recipes.filter(custom_filter).order_by("-pub_date")
    # настраиваем paginator
    paginator = Paginator(recipes, OBJ_ON_PAGE)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)
    # задаем контекст
    context = {
        "recipes": recipes,
        "tags": tags,
        "page": page,
        "paginator": paginator,
        "url_name": "profile",
        "title": author.get_full_name,
        "author": author,
    }
    return render(request, "index.html", context)


@login_required
def subscribes_view(request):
    user = get_object_or_404(User, username=request.user)
    cards = user.subscribes.prefetch_related("author__recipes").order_by(
        "author__first_name"
    )
    paginator = Paginator(cards, OBJ_ON_PAGE)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "tags": [],
        "paginator": paginator,
        "url_name": "subscribes",
        "title": "Мои подписки",
    }
    return render(request, "subscribe.html", context)


@login_required
def shop_list_view(request):
    user = get_object_or_404(User, username=request.user)
    shoplist = user.shop_list.select_related("recipe")
    context = {
        "title": "Список покупок",
        "url_name": "shop_list",
        "shoplist": shoplist,
    }
    return render(request, "shopList.html", context)


@login_required
def generate_pdf_view(request):
    reportlab.rl_config.TTFSearchPath.append(
        str(settings.BASE_DIR) + "/Library/Fonts/"
    )
    user = get_object_or_404(User, username=request.user)
    ing_dict = {}
    shop_list = user.shop_list.select_related("recipe")
    if not shop_list:
        redirect('shop_list')
    # генерируем словарь с ингредиентами
    for el in shop_list:
        ingredients = el.recipe.ingredients.select_related("ingredient")
        for ingredient in ingredients:
            name = ingredient.ingredient.title
            count = ingredient.count
            dimension = ingredient.ingredient.dimension
            if name not in ing_dict:
                ing_dict[name] = [count, dimension]
            else:
                ing_dict[name][0] += count
    # настройка pdf файла и ответа на выгрузку файла
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="shopList.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
    p.setFont("Arial", 20)
    x = 50
    y = 750
    for num, el in enumerate(ing_dict):
        # если закончилось место на странице создаем новую страницу
        if y <= 100:
            y = 700
            p.showPage()
            p.setFont("Arial", 20)
        p.drawString(
            x, y, f"№{num + 1}: {el} - {ing_dict[el][0]} {ing_dict[el][1]}"
        )
        y -= 30
    p.showPage()
    p.save()
    return response


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


class Tech(TemplateView):
    template_name = "static_templates/technologies.html"


class About(TemplateView):
    template_name = "static_templates/about_me.html"
