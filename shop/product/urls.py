from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('category/<slug:cat_slug>', views.index, name='category'),
    path('brand/<slug:brand_slug>/', views.brand_page, name='brand'),
    path('search_results/', views.SearchResultsView.as_view(), name='search_results'),
    path('product/<slug:product_slug>/',
         views.product_detail,
         name='product_detail'
         )
]