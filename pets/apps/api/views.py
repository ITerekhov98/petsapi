from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from pets.apps.main.models import Pet
from .serializers import PetSerializer


class PetsViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_queryset(self):
        limit = int(self.request.query_params.get('limit', 20))
        offset = int(self.request.query_params.get('offset', 0))
        queryset =  Pet.objects.all().order_by('-created_at')[offset:limit+offset]
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": Pet.objects.count(),
            "items": serializer.data
            }
        )

