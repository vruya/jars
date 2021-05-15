from rest_framework import exceptions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer, OrderItem, Order, Product


class CategoryProductViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects

    def list(self, request, category_slug=None):
        filters = {'categories__slug': category_slug}
        
        if request.GET.get('filter',None) == 'without_order':
            filters.update({'orderitem__isnull': True})

        serializer = self.serializer_class(self.queryset.prefetch_related('categories', 'orderitem').filter(**filters), many=True)
        return Response(serializer.data)

