from rest_framework import routers
from django.urls import path, include

from .views import ProductViewSet, CategoryViewSet, StoreViewSet, FeedbackViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'feedbacks', FeedbackViewSet,)

urlpatterns = [
    path('', include(router.urls)),
]
