from django.urls import path

from . import views


urlpatterns = [
    path('', views.add_review_to_cite, name='add_review'),

    ]
