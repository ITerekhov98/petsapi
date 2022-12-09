from rest_framework import serializers

from pets.apps.main.models import Pet, PetPhoto
from django.contrib.sites.models import Site

class PetPhotoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = PetPhoto
        fields = (
            'id',
            'url',
        )
   
    def get_url(self, obj):
        request = self.context.get('request')
        url = obj.photo.url
        return request.build_absolute_uri(url)


class PetSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    photos = PetPhotoSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%dT%H:%M:%S"
    )
    
    class Meta:
        model = Pet
        fields = (
            'id',
            'name',
            'age',
            'type',
            'photos',
            'created_at',
        )


class PetPhotoCLISerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = PetPhoto
        fields = (
            'url',
        )

    def get_url(self, obj):
        url = obj.photo.url
        return f"https://{Site.objects.get_current().domain}{url}"


class PetCLISerializer(PetSerializer):
    photos = PetPhotoCLISerializer(many=True, read_only=True)