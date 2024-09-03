from rest_framework import serializers
from teequeapp.models import *
from decimal import Decimal

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'user', 'skills', 'portfolio', 'average_rating', 'number_of_reviews']


class ServiceSerializer(serializers.ModelSerializer):
    taxedPrice = serializers.SerializerMethodField(method_name='price_w_tax')
    category_id = CategorySerializer(read_only=True)
    seller_id = SellerSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    def price_w_tax(self, service: Service):
        return (service.price * Decimal(0.15)) + service.price

    class Meta:
        model = Service
        exclude = ['created_at', 'updated_at']