from rest_framework import routers
from django.urls import path, include

from .views import ProductViewSet, CategoryViewSet, StoreViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'stores', StoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
