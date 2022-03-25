from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from product.models import Product, Category, Store
from .serializers import ProductSerializer, CategorySerializer, \
    StoreSerializer, CommentSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        return product.feedbacks.all()

