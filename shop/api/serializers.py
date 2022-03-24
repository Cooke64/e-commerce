from rest_framework import serializers

from product.models import Product, COLOR_CHOICES, SIZE_CHOICES


class ProductSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=COLOR_CHOICES)
    size = serializers.ChoiceField(choices=SIZE_CHOICES)
    brand = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'price', 'category', 'available',
                  'color', 'size']
