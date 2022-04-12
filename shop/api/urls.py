from rest_framework import routers
from django.urls import path, include

from .views import ProductViewSet, CategoryViewSet, StoreViewSet, FeedbackViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='all_product')
router.register(r'categories', CategoryViewSet, basename='all_categories')
router.register(r'stores', StoreViewSet, basename='all_stores')
router.register(r'feedbacks', FeedbackViewSet, basename='all_feedbacks')

urlpatterns = [
    path('', include(router.urls)),
]
