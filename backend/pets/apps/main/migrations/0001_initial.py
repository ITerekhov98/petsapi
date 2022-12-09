# Generated by Django 4.1.4 on 2022-12-08 12:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Имя питомца')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('type', models.CharField(choices=[('dog', 'Собака'), ('cat', 'Кошка')], db_index=True, max_length=10, verbose_name='Вид животного')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Питомец',
                'verbose_name_plural': 'Питомцы',
            },
        ),
    ]