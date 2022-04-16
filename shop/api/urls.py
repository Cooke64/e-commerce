from rest_framework import routers
from django.urls import path, include

from .views import ProductViewSet, CategoryViewSet, StoreViewSet, \
    FeedbackViewSet, FavoriteViewSet, CustomerViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet,)
router.register(r'categories', CategoryViewSet,)
router.register(r'stores', StoreViewSet,)
router.register(r'feedback/', FeedbackViewSet, basename='feedbacks')
router.register(r"favorite", FavoriteViewSet, basename="favorite")
router.register(r'customer', CustomerViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
