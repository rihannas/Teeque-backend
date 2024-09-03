from django_filters.rest_framework import FilterSet
from teequeapp.models import Service

class ServiceFilter(FilterSet):
  class Meta:
    model = Service
    fields = {
      'category_id': ['exact'],
      'price': ['gt', 'lt']
    }