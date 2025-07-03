from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CatalogRAGQueryViewSet

router = DefaultRouter()
router.register('catalog-rag', CatalogRAGQueryViewSet, basename='catalogragquery')

urlpatterns = [
    path('', include(router.urls)),
]
