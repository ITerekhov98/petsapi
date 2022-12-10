import uuid
from typing import Union

from pets.apps.main.models import Pet

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def delete_pets_ids_with_validation(pets_ids: Union[list, tuple]) -> tuple:
    '''Принимает список id питомцев, проводит валидацию и проверку в БД.
       Возвращает список невалидных id с указанием причины.
    '''

    errors_description = {
        '404': 'Pet with the matching ID was not found.',
        '400': 'Invalid pet ID'
    }

    invalid_ids = [
        {
            'id': pet_id,
            'error': errors_description['400']
        }
        for pet_id in pets_ids if not is_valid_uuid(pet_id)
    ]
    non_exist_ids = Pet.objects.delete_by_ids(
        [pet_id for pet_id in pets_ids if is_valid_uuid()]
    )
    invalid_ids.extend(
        {
            'id': pet_id,
            'error': errors_description['404']
        }
        for pet_id in non_exist_ids
    )
    return invalid_ids
