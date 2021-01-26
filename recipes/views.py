from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView

from .forms import RecipeForm


def index(request):
    return render(request, 'index.html')


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            return redirect('index')
        return render(request, 'formRecipe.html', context)
    return render(request, 'formRecipe.html', context)
