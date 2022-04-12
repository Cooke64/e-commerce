from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from customer.models import User
from product import models
from product.models import Feedback, Store, Likes, Product, Favorite


class StoreSerializer(serializers.ModelSerializer):
    product_item = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = models.Store
        fields = ['name', 'product_item']


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = models.Category
        fields = ['name', 'slug', 'products']


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Feedback
        fields = ['user', 'product', 'text', 'score']


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ('name', 'price', 'available', 'url')


class FeedbackProductSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов для отображения товара"""
    class Meta:
        model = Feedback
        fields = ['text', 'score']


class StoreProductSerializer(serializers.ModelSerializer):
    """Сериализатор магазина для отображения товара"""
    class Meta:
        model = models.Store
        fields = ['name',]


class ProductSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=models.COLOR_CHOICES)
    size = serializers.ChoiceField(choices=models.SIZE_CHOICES)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    shop = StoreProductSerializer(read_only=True, many=True)
    feedbacks = FeedbackProductSerializer(read_only=True, many=True)
    total_feedback = serializers.SerializerMethodField()
    total_shops = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ['name', 'brand', 'price', 'category', 'available',
                  'color', 'size', 'shop', 'feedbacks', 'total_feedback', 'total_shops',
                  'total_likes', 'url'
                  ]

    def get_total_feedback(self, obj):
        return Feedback.objects.filter(pk=obj.pk).count()

    def get_total_shops(self, obj):
        return Store.objects.filter(product_item=obj.pk).count()

    def get_total_likes(self, obj):
        return Likes.objects.filter(products=obj.pk).count()


class FaveSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Product.objects.all(),
    )
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Favorite
        fields = '__all__'
