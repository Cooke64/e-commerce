from rest_framework import serializers

from product import models
from product.models import Feedback


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=models.COLOR_CHOICES)
    size = serializers.ChoiceField(choices=models.SIZE_CHOICES)
    category = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    shop = StoreSerializer(read_only=True, many=True)

    class Meta:
        model = models.Product
        fields = ['name', 'brand', 'price', 'category', 'available',
                  'color', 'size', 'shop']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Feedback
        fields = '__all__'
