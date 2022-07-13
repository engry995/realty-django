from django.contrib.auth.models import User
from django.db import models
from pathlib import Path

from django.urls import reverse


def path_for_foto(instance, file_name):
    return Path('house') / instance.house.owner.username / file_name


class Type(models.Model):
    title = models.CharField(max_length=30, verbose_name='Тип жилья', unique=True)
    description = models.CharField(max_length=150, verbose_name='Описание типа', blank=True)

    class Meta:
        verbose_name = 'Тип жилья'
        verbose_name_plural = 'Типы жилья'

    def __str__(self):
        return f'Тип жилья: {self.title}'


class Rooms(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name='Количество комнат')
    description = models.CharField(max_length=150, verbose_name='Описание комнат', blank=True)

    class Meta:
        verbose_name = 'Комнаты'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'{self.number} ({self.description})'


class House(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Собственник', related_name='house')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Тип жилья', related_name='house')
    rooms = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Комнаты', related_name='house')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.PositiveIntegerField(verbose_name='Стоимость', blank=True, null=True)
    actual = models.BooleanField(default=True, verbose_name='Предложение активно')

    class Meta:
        verbose_name = 'Жилье'
        verbose_name_plural = 'Жилье'

    def __str__(self):
        return f'{self.title} ({self.price})'

    def get_absolute_url(self):
        return reverse('house_detail', args=[self.pk])


class HouseFoto(models.Model):

    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='foto', verbose_name='Жилье')
    foto = models.ImageField(blank=False, upload_to=path_for_foto, verbose_name='Фотография')

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    def __str__(self):
        return f'Фото {self.foto.name}'
