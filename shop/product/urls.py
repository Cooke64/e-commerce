from django.urls import path

from . import views

urlpatterns = [

    path('', views.product_list, name='index'),

    path('category/<slug:cat_slug>', views.product_list, name='category'),
    path('search_results/',
         views.SearchResultsView.as_view(),
         name='search_results'),
    path('product/<slug:product_slug>/',
         views.product_detail,
         name='product_detail'
         ),
    path('product/<slug:product_slug>/feedback/',
         views.add_feedback,
         name='add_feedback'),
    path('favorites_items/', views.favorites_items, name='favorites_items'),
    path(
        'product/<slug:product_slug>/add_item_in_fav/',
        views.add_item_in_fav,
        name='add_item_in_fav'
    ),
    path(
        'product/<slug:product_slug>/stop_being_fav/',
        views.stop_being_fav,
        name='stop_being_fav'
    ),
    path(
        'product/<slug:product_slug>/add_score/',
        views.add_score,
        name='add_score'
    ),
]