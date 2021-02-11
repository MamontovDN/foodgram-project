from django.urls import path

from . import views

urlpatterns = [
    path('genpdf/', views.generate_pdf_view, name='generate_pdf'),
    path('shoplist/', views.shop_list_view, name='shop_list'),
    path('newrecipe/', views.new_recipe, name='new_recipe'),
    path('recipe/edit/<int:recipe_id>/', views.new_recipe, name='recipe_edit'),
    path('recipe/delete/<int:recipe_id>', views.recipe_delete,
         name='recipe_delete'),
    path('subscribes/', views.subscribes_view, name='subscribes'),
    path('profile/<int:author_id>/', views.profile, name='profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('recipe/<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    path('spec/', views.Tech.as_view(), name='spec'),
    path('about-me/', views.About.as_view(), name='about-me'),
    path('', views.index, name='index'),

]
