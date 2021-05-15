from django.urls import path

from .views import CategoryProductViewSet

urlpatterns = [

    path('categories/<str:category_slug>/products', CategoryProductViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }))

]
