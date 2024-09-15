from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import ProtectedError

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

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(service_id=kwargs['pk']).exclude(order_status=OrderItem.ORDER_STATUS_COMPLETE).count() > 0:
            return Response({'error': 'Service cannot be deleted because it is associated as an active order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    def get_queryset(self):
        service_id = self.kwargs.get('service_pk')
        return Rating.objects.select_related('buyer__user').filter(service_id=service_id)



class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.select_related('user').all()
    serializer_class = SellerSerializer
    lookup_field = 'pk'

    # make sure this url is accessed if user is a seller object or else anyone can create a seller object since we are using get_or_create method

    @action(detail=False, methods=['GET', 'POST'])
    def me(self, request):
        (seller, created) = Seller.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = SellerSerializer(seller)
            return Response(serializer.data)
        
        # TODO: implement this
        # elif request.method == 'PUT':
        #     serializer = SellerSerializer(seller)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     return Response(serializer.data)

class BuyerViewSet(ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

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
        
        # TODO: implement this
        # elif request.method == 'PUT':
        #     serializer = BuyerSerializer(buyer, data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     return Response(serializer.data)


