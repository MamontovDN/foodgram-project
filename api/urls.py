from django.urls import path

from . import views

urlpatterns = [
    path('ingredients/', views.IngredientViewSet.as_view(),
         name='api_ingredient'),
    path('favorites/', views.FavoritesView.as_view(),
         name='api_add_favorites'),
    path('favorites/<int:id>/', views.FavoritesView.as_view(),
         name='api_del_favorites'),
    path('subscriptions/', views.SubscribeView.as_view(),
         name='api_add_subscribe'),
    path('subscriptions/<int:id>/', views.SubscribeView.as_view(),
         name='api_del_subscribe'),
    path('purchases/', views.ShopListView.as_view(), name='api_purchase'),
    path('purchases/<int:id>/', views.ShopListView.as_view(),
         name='api_del_purchases'),
]
