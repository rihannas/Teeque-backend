from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, permission_classes


from teequeapp.models import *
from .serializers import *
from .filters import *


# Create your views here.
class ServiceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Service.objects.select_related('category', 'seller').prefetch_related('tags').all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price'] #there should be ordering by ratings too

    # def delete(self, request, pk):
    #     try:
    #         service = get_object_or_404(Service, pk=pk)
    #         if service.orderitems.exists():
    #             return Response(
    #                 {'error': 'Service cannot be deleted because it is associated with an order item.'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         service.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         return Response(
    #             {'error': 'An unexpected error occurred.', 'detail': str(e)},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )


class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.select_related('user').all()
    serializer_class = SellerSerializer

    lookup_field = 'pk'


class BuyerViewSet(ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

    @action(detail=True)
    def history(self, request, pk):
        return Response('ok')

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
