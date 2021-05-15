from rest_framework import exceptions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects
    
    def list(self, request):
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

    def update(self, request, pk=None):
        serializer = self.serializer_class(instance=self.queryset.get(id=pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response( serializer.data, status.HTTP_202_ACCEPTED)

    def partial_update(self, request, pk=None):
        serializer = self.serializer_class(instance=self.queryset.get(id=pk), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        try:
            self.queryset.filter(id__in=request.data['ids']).delete()
        except KeyError:
            self.queryset.get(id=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
