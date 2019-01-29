from rest_framework import serializers

from products.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'sku', 'category', 'description', 'price',
                  'created', 'featured',)
