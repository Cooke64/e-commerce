from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductView.as_view(), name='products'),
    path('add_product', views.product_add, name='add_product'),
    path('edit_product/<slug:product_slug>', views.edit_product, name='edit_product'),
    path('json/<int:product_pk>/', views.get_json_response, name='json'),
    ]
