import shutil
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.conf import settings

from ..models import Type, Rooms, House, HouseFoto


class TypeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Type.objects.create(title='Тип', description='Тип жилья')

    def test_fields_label(self):
        type_test = Type.objects.get(id=1)
        self.assertEqual(Type._meta.get_field('title').verbose_name, 'Тип жилья')
        self.assertEqual(Type._meta.get_field('description').verbose_name, 'Описание типа')

    def str_method(self):
        type_test = Type.objects.get(id=1)
        self.assertEqual(str(type_test), 'Тип жилья: Тип')

    def test_meta(self):
        self.assertEqual(Type._meta.verbose_name, 'Тип жилья')
        self.assertEqual(Type._meta.verbose_name_plural, 'Типы жилья')


class RoomsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Rooms.objects.create(number=1, description='Однокомнатная квартира')

    def test_fields_label(self):
        rooms = Rooms.objects.get(id=1)
        self.assertEqual(Rooms._meta.get_field('number').verbose_name, 'Количество комнат')
        self.assertEqual(Rooms._meta.get_field('description').verbose_name, 'Описание комнат')

    def str_method(self):
        rooms = Rooms.objects.get(id=1)
        self.assertEqual(str(rooms), '1 (Однокомнатная квартира)')

    def test_meta(self):
        self.assertEqual(Rooms._meta.verbose_name, 'Комнаты')
        self.assertEqual(Rooms._meta.verbose_name_plural, 'Комнаты')


class HouseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        type_test = Type.objects.create(title='Тип', description='Тип жилья')
        rooms = Rooms.objects.create(number=1, description='Однокомнатная квартира')
        cls.house = House.objects.create(owner=user, title='Объявление',
                                         type=type_test, rooms=rooms,
                                         description='Однокомнатная квартира',
                                         price=1e6, actual=True)

    def test_fields_label(self):
        house = House.objects.get(id=1)
        self.assertEqual(house._meta.get_field('owner').verbose_name, 'Собственник')
        self.assertEqual(house._meta.get_field('title').verbose_name, 'Заголовок')
        self.assertEqual(house._meta.get_field('type').verbose_name, 'Тип жилья')
        self.assertEqual(house._meta.get_field('rooms').verbose_name, 'Комнаты')
        self.assertEqual(house._meta.get_field('description').verbose_name, 'Описание')
        self.assertEqual(house._meta.get_field('price').verbose_name, 'Стоимость')
        self.assertEqual(house._meta.get_field('actual').verbose_name, 'Предложение активно')

    def str_method(self):
        house = House.objects.get(id=1)
        self.assertEqual(str(house), 'Объявление (1000000)')

    def test_meta(self):
        self.assertEqual(House._meta.verbose_name, 'Жилье')
        self.assertEqual(House._meta.verbose_name_plural, 'Жилье')


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class HouseFotoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_foto = SimpleUploadedFile('foto.jpg', b'fff', content_type='image/jpeg')
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        house = House.objects.create(owner=user, title='Объявление')
        HouseFoto.objects.create(house=house, foto=test_foto)

    def test_fields_label(self):
        house_foto = HouseFoto.objects.get(id=1)
        self.assertEqual(house_foto._meta.get_field('house').verbose_name, 'Жилье')
        self.assertEqual(house_foto._meta.get_field('foto').verbose_name, 'Фотография')

    def str_method(self):
        house_foto = HouseFoto.objects.get(id=1)
        self.assertEqual(str(house_foto), 'Фото foto.jpg')

    def test_meta(self):
        self.assertEqual(HouseFoto._meta.verbose_name, 'фотография')
        self.assertEqual(HouseFoto._meta.verbose_name_plural, 'фотографии')


    def test_path_for_foto(self):
        house_foto = HouseFoto.objects.get(id=1)
        path_foto = house_foto.foto.url
        self.assertEqual(path_foto, '/media/house/nik/foto.jpg')


    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()
