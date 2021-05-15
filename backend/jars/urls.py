from django.urls import path

from .views import JarViewSet, OperationViewSet

urlpatterns = [

    path('jars', JarViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='jars'),

    path('jars/<str:pk>', JarViewSet.as_view({
       'get': 'retrieve',
        'delete': 'destroy'
    }), name='jars'),

    path('operations', OperationViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='operations'),
    
    path('operations/<str:pk>', OperationViewSet.as_view({
       'get': 'retrieve'
    }), name='operations'),

]
