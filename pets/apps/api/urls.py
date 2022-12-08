from django.urls import path, include
from rest_framework import routers

from .views import PetsViewSet


router = routers.SimpleRouter()
router.register(r'pets', PetsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]