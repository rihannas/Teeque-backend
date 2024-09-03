from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter

from .views import *

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')

# Nested routers
services_router = NestedSimpleRouter(router, r'services', lookup='service')
services_router.register(r'services',  ServiceViewSet, basename='services')

urlpatterns = [
  path('', include(router.urls))
]  
