from django.shortcuts import render
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from teequeapp.models import *
from .serializers import *
from .filters import *


# Create your views here.
class ServiceViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Service.objects.select_related('category_id', 'seller_id').prefetch_related('tags').all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price'] #there should be ordering by ratings too


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.select_related('user').all()
    serializer_class = SellerSerializer

    lookup_field = 'id'