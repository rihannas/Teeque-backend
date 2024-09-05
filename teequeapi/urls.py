from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from .views import *

# Main router
router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'sellers', SellerViewSet, basename='sellers')
router.register(r'buyers', BuyerViewSet, basename='buyers')

# Nested routers
service_router = NestedSimpleRouter(router, r'services', lookup='service')
service_router.register(r'reviews', RatingViewSet, basename='service-reviews')

seller_router = NestedSimpleRouter(router, r'sellers', lookup='seller')
seller_router.register(r'services', ServiceViewSet, basename='seller-services')

urlpatterns = router.urls + service_router.urls + seller_router.urls
