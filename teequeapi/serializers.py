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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'skills', 'portfolio', 'average_rating', 'number_of_reviews']


class BuyerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Buyer
        fields = ['id', 'favorite_services', 'user']

class BuyerRatingSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    
    class Meta:
        model = Buyer
        fields = ['id', 'user'] 

class RatingSerializer(serializers.ModelSerializer):
    buyer = BuyerRatingSerializer(read_only=True)
    class Meta:
        model = Rating
        fields = ['created_at', 'buyer', 'rating', 'comment']



class ServiceSerializer(serializers.ModelSerializer):
    taxedPrice = serializers.SerializerMethodField(method_name='price_w_tax')
    category = serializers.StringRelatedField()
    seller = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='teequeapi:sellers-detail',
        lookup_field='pk'
    )
    tags = TagSerializer(many=True, read_only=True)

    def price_w_tax(self, service: Service):
        return (service.price * Decimal(0.15)) + service.price
    

    class Meta:
        model = Service
        exclude = ['created_at', 'updated_at']

