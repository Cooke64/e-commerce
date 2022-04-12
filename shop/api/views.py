from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser


from product.models import Product, Category, Store, Feedback
from .serializers import ProductSerializer, CategorySerializer, \
    StoreSerializer, FeedbackSerializer, ProductListSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = LimitOffsetPagination
    filterset_fields = ('color', 'size', 'price')
    search_fields = ('@name', '@shop__name', '@brand__name')
    ordering_fields = ('price', )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = (IsAdminUser,)


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        post = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        return post.feedbacks.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, product_id=self.kwargs.get("product_id")
        )
