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
    average_rating = serializers.ReadOnlyField()
    number_of_reviews = serializers.ReadOnlyField()
    about = serializers.CharField(source='user.about', required=False)

    class Meta:
        model = Seller
        fields = ['id', 'about', 'skills', 'portfolio', 'average_rating', 'number_of_reviews']
    
    def create(self, validated_data):
        requester_user = self.context['request'].user
        about = validated_data.pop('about', None)
        user = validated_data.pop('user', None)

        if about:
            requester_user.about = about
            requester_user.save()

        seller, created = Seller.objects.get_or_create(user=requester_user, **validated_data)

        if created:
        # seller instance already exists, so we can update or return it
            return seller.save()
    
        # If created, return the newly created seller
        return seller
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        about = user_data.get('about')
        if about:
            instance.user.about = about
            instance.user.save()
        return super().update(instance, validated_data)

class BuyerSerializer(serializers.ModelSerializer):
    about = serializers.CharField(source='user.about', required=False)
    
    class Meta:
        model = Buyer
        fields = ['id', 'about']

    def create(self, validated_data):
        requester_user = self.context['request'].user
        about = validated_data.pop('about', None)

        if about:
            requester_user.about = about
            requester_user.save()

        buyer, created = Buyer.objects.get_or_create(user=requester_user)

        if created:
        # Buyer instance already exists, so we can update or return it
            return buyer.save()
    
    # If created, return the newly created buyer
        return buyer
    
    def update(self, instance, validated_data):
        """"""
        user_data = validated_data.pop('user', {})
        about = user_data.get('about')
        if about:
            instance.user.about = about
            instance.user.save()
        return super().update(instance, validated_data)

        

    
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


class ServiceSellerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Seller
        fields = ['username', 'average_rating']


class ServiceSerializer(serializers.ModelSerializer):
    taxedPrice = serializers.SerializerMethodField(method_name='price_w_tax')
    seller_info = ServiceSellerSerializer(source='seller', read_only=True)
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
