from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from product.models import Product, Category, Store, Feedback
from .serializers import ProductSerializer, CategorySerializer, \
    StoreSerializer, FeedbackSerializer, ProductListSerializer, FaveSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Вывод всех продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = LimitOffsetPagination
    filterset_fields = ('color', 'size', 'price')
    search_fields = ('@name', '@shop__name', '@brand__name')
    ordering_fields = ('price', )

    def get_serializer_class(self):
        """Если запрос к списку продуктов, то используем ProductListSerializer,
        если требуется отобразить detail product ProductSerializer
        """
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    @action(detail=False, url_path='product_with_review')
    def get_product_with_feedback(self, request):
        """Отображение продуктов только с отзывами."""
        products = (Product.objects
                    .filter(feedbacks__isnull=False)
                    .distinct())
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """Категории товаров."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class StoreViewSet(viewsets.ModelViewSet):
    """Магазины товаров."""
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = (IsAdminUser,)


class FeedbackViewSet(viewsets.ModelViewSet):
    """Отзывы конкретного товара"""
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        if self.action == 'list':
            post = Feedback.objects.all()
        else:
            post_detail = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
            post = post_detail.feedbacks.all()
        return post

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, product_id=self.kwargs.get("product_id")
        )


class FavoriteViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = FaveSerializer
    permissions_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        new_queryset = self.request.user.who_likes_items.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
