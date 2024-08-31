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
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    taxedPrice = serializers.SerializerMethodField(method_name='price_w_tax')
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    def price_w_tax(self, service: Service):
        return (service.price * Decimal(0.15)) + service.price

    class Meta:
        model = Service
        exclude = ['created_at', 'updated_at']