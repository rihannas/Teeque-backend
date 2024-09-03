from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter

from .views import *

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'sellers', SellerViewSet, basename='sellers')


# Nested routers
service_router = NestedSimpleRouter(router, r'services', lookup='service')
service_router.register(r'services',  ServiceViewSet, basename='services')

seller_router = NestedSimpleRouter(router, r'sellers', lookup='seller')
seller_router.register(r'seller',  SellerViewSet, basename='sellers')


urlpatterns = [
  path('', include(router.urls))
]  
