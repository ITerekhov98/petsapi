import json

from distutils.util import strtobool
from django.core.management.base import BaseCommand

from pets.apps.main.models import Pet
from pets.apps.api.serializers import PetCLISerializer


class Command(BaseCommand):
    help = 'Dump info about pets to json file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--has-photos',
            help='''
            Set "true" if you need only instances with photos, "false" otherwise.
            Keeping argument undefined will catch all instances.
            ''',
        )

    def handle(self, *args, **options):
        has_photos = options.get('has_photos')
        if not has_photos:
            pets = Pet.objects.all()
        else:
            has_photos = strtobool(has_photos)
            has_not_photos = False if has_photos else True
            pets = Pet.objects.filter(photos__isnull=has_not_photos) \
                              .distinct() \
                              .order_by('-created_at') \

        serialized_pets = PetCLISerializer(pets, many=True).data
        self.stdout.write(json.dumps(serialized_pets))
