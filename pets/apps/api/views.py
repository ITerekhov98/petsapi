from distutils.util import strtobool

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError

from pets.apps.main.models import Pet, PetPhoto
from .serializers import PetSerializer, PetPhotoSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class PetsViewSet(viewsets.ModelViewSet):
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_queryset(self):
        limit = int(self.request.query_params.get('limit', 20))
        offset = int(self.request.query_params.get('offset', 0))
        has_photos = self.request.query_params.get('has_photos')
        if not has_photos:
            queryset = Pet.objects.all().order_by('-created_at')[offset:limit+offset]
        else:
            has_photos = strtobool(has_photos)
            has_not_photos = False if has_photos else True
            queryset = Pet.objects.filter(photos__isnull=has_not_photos) \
                                  .distinct() \
                                  .order_by('-created_at') \
                                  [offset:limit+offset]
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
    
    @action(detail=True, methods=['post'])
    def upload_photo(self, request, pk=None):
        try:
            photo = request.data['media']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        pet = get_object_or_404(Pet, id=pk)
        pet_photo = PetPhoto.objects.create(
            pet=pet,
            photo=photo
        )
        response = PetPhotoSerializer(pet_photo, context={"request": request}).data
        return Response(response)
    



