import uuid
from django.db import models
from django.core.validators import MinValueValidator

class PetQuerySet(models.QuerySet):

    def delete_by_ids(self, pets_ids):
        '''Принимает список c id объектов, удаляет их и возвращает id
           несуществовавших объектов
        '''
        valid_pets_ids = [
            str(pets_id) for pets_id in 
            self.filter(id__in=pets_ids).values_list(flat=True)
        ]
        invalid_pets_ids = list(set(pets_ids) - set(valid_pets_ids))
        self.filter(id__in=valid_pets_ids).delete()
        return invalid_pets_ids


class Pet(models.Model):
    class PetType(models.TextChoices):
        DOG = 'dog', 'Собака'
        CAT = 'cat', 'Кошка'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(verbose_name='Имя питомца', max_length=100)
    age = models.IntegerField(
        verbose_name='Возраст',
        validators = [MinValueValidator(0)]
    )
    type = models.CharField(
        verbose_name='Вид животного',
        max_length=10,
        choices=PetType.choices,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PetQuerySet.as_manager()

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = "Питомцы"

    def __str__(self) -> str:
        return f'{self.type}: {self.name}'


class PetPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(
        Pet,
        verbose_name='Питомец',
        related_name='photos',
        on_delete=models.CASCADE
    )
    photo = models.ImageField('Фото', upload_to='pets')

    class Meta:
        verbose_name = 'Фото питомца'
        verbose_name_plural = "Фото Питомцев"
