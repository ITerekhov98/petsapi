from rest_framework import serializers

from pets.apps.main.models import Pet

class PetSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Pet
        fields = (
            'id',
            'name',
            'age',
            'type',
            'created_at'
        )