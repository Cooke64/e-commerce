from django.urls import path

from . import views


urlpatterns = [
    path('', views.product_add, name='add_product'),
    ]
