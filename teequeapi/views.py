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

    def delete(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        try:
            service.delete()
            if service.orderitems.count() > 0:
                return Response({'success': 'Service is deleted'}, status=status.HTTP_204_NO_CONTENT)

        except ProtectedError:
                return Response({'error': 'Service cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    def get_queryset(self):
        service_id = self.kwargs.get('service_pk')
        return Rating.objects.select_related('buyer__user').filter(service_id=service_id)



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
        # elif request.method == 'PUT':
        #     serializer = BuyerSerializer(buyer, data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     return Response(serializer.data)


