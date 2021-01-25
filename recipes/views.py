from django.shortcuts import render
from django.views.generic import CreateView


def index(request):
    return render(request, 'index.html')


def new_recipe(request):
    return render(request, 'formRecipe.html')