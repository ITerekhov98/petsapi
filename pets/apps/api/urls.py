from django.urls import path, include
from rest_framework import routers

from .views import PetsViewSet

class CustomRouter(routers.SimpleRouter):
    routes = [
        # List route.
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'delete': 'destroy'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        routers.DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
    
router = CustomRouter()
router.register(r'pets', PetsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]