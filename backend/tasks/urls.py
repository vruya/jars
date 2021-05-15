from django.urls import path

from .views import TaskViewSet

urlpatterns = [
    path('tasks', TaskViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='tasks'),
   path('tasks/<str:pk>', TaskViewSet.as_view({
       'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='tasks'),

]
