from rest_framework import serializers

from product import models
from product.models import Feedback, Store


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
    product = serializers.StringRelatedField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feedback
        fields = ['user', 'product', 'text']


class ProductSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=models.COLOR_CHOICES)
    size = serializers.ChoiceField(choices=models.SIZE_CHOICES)
    category = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    shop = StoreSerializer(read_only=True, many=True)
    feedbacks = FeedbackSerializer(read_only=True, many=True)
    total_feedback = serializers.SerializerMethodField()
    total_shops = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ['name', 'brand', 'price', 'category', 'available',
                  'color', 'size', 'shop', 'feedbacks', 'total_feedback', 'total_shops']

    def get_total_feedback(self, obj):
        return Feedback.objects.filter(pk=obj.pk).count()

    def get_total_shops(self, obj):
        return Store.objects.filter(product_item=obj.pk).count()
