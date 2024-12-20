from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import ProtectedError
from django.db import transaction

from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin 
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, permission_classes

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

import os

from teequeapp.models import *
from .serializers import *
from .filters import *
from .permissions import IsServiceSellerOrReadOnly
from .signals import *


# Create your views here.

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.getenv('CALLBACK_URL_YOU_SET_ON_GOOGLE')
    client_class = OAuth2Client


class RegistrationProgressViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RegistrationProgressSerializer
    
    def list(self, request):
        """Get registration progress"""
        progress = request.user.registration_progress
        serializer = self.get_serializer(progress)
        return Response(serializer.data)

class ProfileViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    @transaction.atomic
    def create(self, request):
        """Complete user profile"""
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            # Update progress
            progress = user.registration_progress
            progress.profile_complete = True
            progress.save()
            
            return Response({
                'message': 'Profile details saved successfully',
                'progress': RegistrationProgressSerializer(progress).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTypeViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        user_type = self.request.data.get('user_type')
        return SellerSerializer if user_type == 'seller' else BuyerSerializer
    
    @transaction.atomic
    def create(self, request):
        """Select user type and create corresponding profile"""
        user = request.user
        user_type = request.data.get('user_type')
        
        if user_type not in ['seller', 'buyer']:
            return Response(
                {'error': 'Invalid user type. Must be either "seller" or "buyer"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Determine model based on user type
        model = Seller if user_type == 'seller' else Buyer
        serializer = self.get_serializer(data=request.data.get('profile_data', {}))
        
        if serializer.is_valid():
            instance = model.objects.create(user=user, **serializer.validated_data)
            
            # Update progress
            progress = user.registration_progress
            progress.type_selection_complete = True
            progress.save()
            
            return Response({
                'message': f'{user_type.title()} profile created successfully',
                'progress': RegistrationProgressSerializer(progress).data,
                'profile': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ServiceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Service.objects.select_related('category', 'seller__user', 'seller').prefetch_related('tags').all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price'] #there should be ordering by ratings too
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, IsServiceSellerOrReadOnly]
        
    def perform_create(self, serializer):
        user = self.request.user
        seller = Seller.objects.get(user=user)
        serializer.save(seller=seller)

    def destroy(self, request, *args, **kwargs):
        # needs more working
        if OrderItem.objects.filter(service_id=kwargs['pk']).exclude(order_status=OrderItem.ORDER_STATUS_COMPLETE).count() > 0:
            return Response({'error': 'Service cannot be deleted because it is associated as an active order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    def get_queryset(self):
        service_id = self.kwargs.get('service_pk')
        return Rating.objects.select_related('buyer__user').filter(service_id=service_id)



class SellerViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Seller.objects.select_related('user').all()
    serializer_class = SellerSerializer
    lookup_field = 'pk'
    permission_classes=[IsAuthenticated]
    #TODO: make sure this url is accessed if user is a seller object or else anyone can create a seller object since we are using get_or_create method

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (seller, created) = Seller.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = SellerSerializer(seller)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = SellerSerializer(seller, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class BuyerViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Buyer.objects.select_related('user').prefetch_related('favorite_services').all()
    serializer_class = BuyerSerializer
    permission_classes=[IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True)
    def history(self, request, pk):
        return Response('ok')

    # make sure this url is accessed if user is a buyer object or else anyone can create a buyer object since we are using get_or_create method

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (buyer, created) = Buyer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = BuyerSerializer(buyer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = BuyerSerializer(buyer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

