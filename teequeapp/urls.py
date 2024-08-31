from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = []  + debug_toolbar_urls()
