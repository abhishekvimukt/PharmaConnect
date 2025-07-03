from rest_framework import serializers
from .models import CatalogRAGQuery

class CatalogRAGQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogRAGQuery
        fields = '__all__'
