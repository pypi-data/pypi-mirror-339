# my_django_base/urls.py
from django.urls import path, include
from rest_framework import routers
from . import api_views

# Create a router for REST API endpoints
router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)
# Add other viewsets here

urlpatterns = [
    # Regular app URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # API endpoints
    path('api/', include((router.urls, 'api'))),
    path('api/custom-endpoint/', api_views.custom_endpoint, name='custom-endpoint'),
]