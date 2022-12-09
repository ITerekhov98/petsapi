import uuid
from django.db import models
from django.conf import settings

class Pet(models.Model):
    class PetType(models.TextChoices):
        DOG = 'dog', 'Собака'
        CAT = 'cat', 'Кошка'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='Имя питомца', max_length=100)
    age = models.IntegerField(verbose_name='Возраст')
    type = models.CharField(
        verbose_name='Вид животного',
        max_length=10,
        choices=PetType.choices,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

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