from rest_framework import exceptions, viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from .models import Jar, Operation
from .serializers import JarSerializer, OperationSerializer
import datetime


class JarViewSet(viewsets.ViewSet):
    # method put / patch is not allowed, jar can be changed only by operation
    serializer_class = JarSerializer
    queryset = Jar.objects
    
    def list(self, request):
        print('here?')
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        dash = get_object_or_404(self.queryset.all(), pk=pk)
        serializer = self.serializer_class(dash)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            self.queryset.filter(id__in=request.data['ids']).delete()
        except KeyError:
            self.queryset.get(id=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class OperationViewSet(viewsets.ModelViewSet):
    #cannot change operation or delete, is major thing with history
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = '__all__'
    ordering_fields = '__all__'


    def retrieve(self, request, pk=None):
        dash = get_object_or_404(self.queryset.all(), pk=pk)
        serializer = self.serializer_class(dash)
        return Response(serializer.data)

    def create(self, request):
        request.data['date_start'] = datetime.datetime.now()
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
