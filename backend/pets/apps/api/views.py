from distutils.util import strtobool

from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser

from pets.apps.main.models import Pet, PetPhoto
from .serializers import PetSerializer, PetPhotoSerializer
from .services import delete_pets_ids_with_validation

class PetsViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, MultiPartParser, FileUploadParser]
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
        return Response(
            {
                "count": Pet.objects.count(),
                "items": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def upload_photo(self, request, pk=None):
        photo = request.data.get('file')
        if not photo:
            raise ParseError('Request has no resource file attached.')
        try:
            pet = get_object_or_404(Pet, id=pk)
        except ValidationError:
            raise ParseError('Bad request.')
        pet_photo = PetPhoto.objects.create(
            pet=pet,
            photo=photo
        )
        response = PetPhotoSerializer(
            pet_photo,
            context={"request": request}
        ).data
        return Response(response, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        pets_ids = request.data.get('ids')
        if not pets_ids:
            raise ParseError('Request has no pets to delete.')


        invalid_ids_with_errors = delete_pets_ids_with_validation(pets_ids)
        response = {
            "deleted": len(pets_ids)
            }
        if invalid_ids_with_errors:
            response['deleted'] -= len(invalid_ids_with_errors)
            response['errors'] = invalid_ids_with_errors
        return Response(
            response,
            status=status.HTTP_200_OK
        )
