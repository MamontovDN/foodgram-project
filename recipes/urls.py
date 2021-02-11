from django.urls import path

from . import views

urlpatterns = [
    path('genpdf/', views.generate_pdf_view, name='generate_pdf'),
    path('shoplist/', views.shop_list_view, name='shop_list'),
    path('recipe/edit/<int:recipe_id>/', views.recipe_edit, name='recipe_edit'),
    path('recipe/delete/<int:recipe_id>', views.recipe_delete,
         name='recipe_delete'),
    path('subscribes/', views.subscribes_view, name='subscribes'),
    path('profile/<int:author_id>/', views.profile, name='profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('newrecipe/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    path('', views.index, name='index'),

]
