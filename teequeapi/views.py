from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from teequeapp.models import *
from .serializers import *
from .filters import *


# Create your views here.
class ServiceViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Service.objects.select_related('category', 'seller').prefetch_related('tags').all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price'] #there should be ordering by ratings too

    def delete(self, request, pk):
        product = get_object_or_404(Service, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Service cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.select_related('user').all()
    serializer_class = SellerSerializer

    lookup_field = 'id'