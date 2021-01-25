from django.urls import path

from . import views

urlpatterns = [
    path('newrecipe/', views.new_recipe, name='new_recipe'),
    path('', views.index, name='index'),

]
