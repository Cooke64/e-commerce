from django.db.models import Avg
from rest_framework import serializers

from customer.models import User, Customer
from product import models
from product.models import Feedback, Store, Likes, Product, Favorite


class StoreSerializer(serializers.ModelSerializer):
    """Отображение магазина."""
    product_item = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = models.Store
        fields = ['name', 'product_item']


class CategorySerializer(serializers.ModelSerializer):
    """Отображение категории"""
    products = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = models.Category
        fields = ['name', 'slug', 'products']


class FeedbackSerializer(serializers.ModelSerializer):
    """Отображение отзывов и рейтинга к товару."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Feedback
        fields = ['user', 'text', 'score']


class ProductListSerializer(serializers.ModelSerializer):
    """Вывод полей при отображении всех товаров."""
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
    """Вывод всех полей товара при product_detail."""
    color = serializers.ChoiceField(choices=models.COLOR_CHOICES)
    size = serializers.ChoiceField(choices=models.SIZE_CHOICES)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    shop = StoreProductSerializer(read_only=True, many=True)
    feedbacks = FeedbackProductSerializer(read_only=True, many=True)
    total_feedback = serializers.SerializerMethodField()
    total_shops = serializers.SerializerMethodField()
    avg_likes = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ['name', 'brand', 'price', 'category', 'available',
                  'color', 'size', 'shop', 'feedbacks', 'total_feedback', 'total_shops',
                  'avg_likes', 'url'
                  ]

    def get_total_feedback(self, obj):
        return Feedback.objects.filter(pk=obj.pk).count()

    def get_total_shops(self, obj):
        return Store.objects.filter(product_item=obj.pk).count()

    def get_avg_likes(self, obj):
        product = Product.objects.get(pk=obj.pk)
        return product.likes.aggregate(result=Avg('score'))


class FaveSerializer(serializers.ModelSerializer):
    """Вывод избранных товаров пользователя."""
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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'admin', 'staff', 'is_active']


class CustomerSerializerFull(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(
        UserSerializer, read_only=True, many=True
    )

    class Meta:
        model = Customer
        fields = ['user', 'first_name', 'phone', 'spent_money', 'last_buy']


class CustomerSerializerBasic(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Customer
        fields = ['user', 'first_name', 'phone']
        read_only_fields = ('user',)
