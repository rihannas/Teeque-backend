from django.shortcuts import render
from rest_framework import mixins, viewsets
from teequeapp.models import *
from .serializers import *

# Create your views here.
class ServiceViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Service.objects.select_related('category_id', 'seller_id').prefetch_related('tags').all()
    serializer_class = ServiceSerializer

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.select_related('user').all()
    serializer_class = SellerSerializer
    lookup_field = 'id'