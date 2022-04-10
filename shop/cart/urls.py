from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_cart_detail, name='cart_detail'),
    path('add/<slug:product_slug>', views.add_product_in_cart, name='item_add'),
    path('remove/<slug:product_slug>', views.remove_product_from_cart, name='item_remove'),
]
