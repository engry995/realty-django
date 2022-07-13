import shutil
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from ..models import House, Type, Rooms, HouseFoto


class HouseListViewTest(TestCase):
    number_of_entries = 15  # количество записей для заполнения базы
    house_text = 'Описание квартиры'

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        type_test = Type.objects.create(title='Тип', description='Тип жилья')
        rooms = Rooms.objects.create(number=1, description='Однокомнатная квартира')
        for num in range(cls.number_of_entries):
            House.objects.create(owner=user, title=f'{cls.house_text} {num}',
                                 type=type_test, rooms=rooms,
                                 description='text',
                                 price=1e6, actual=True)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_realty/main.html')

    def test_numbers_blog_in_list_view(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(len(resp.context['house_list']), self.number_of_entries)

    def test_context_in_blog_list_view(self):
        # Проверка, что выведено определенное количество записей
        resp = self.client.get(reverse('main'))
        self.assertContains(resp, self.house_text, self.number_of_entries, status_code=200)


class HouseDetailViewTest(TestCase):
    house_text = 'Описание квартиры'

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        type_test = Type.objects.create(title='Тип', description='Тип жилья')
        rooms = Rooms.objects.create(number=1, description='Однокомнатная квартира')
        House.objects.create(owner=user, title='Объявление',
                             type=type_test, rooms=rooms,
                             description=cls.house_text,
                             price=1e6, actual=True)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/realty/1/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('house_detail', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('house_detail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_realty/house_detail.html')

    def test_context_blog_in_detail_view(self):
        resp = self.client.get(reverse('house_detail', args=[1]))
        self.assertIsNotNone(resp.context.get('house'), msg='Нет переменной шаблона:')

    def test_context_in_blog_list_view(self):
        # Проверка, что выведена запись
        resp = self.client.get(reverse('house_detail', args=[1]))
        self.assertContains(resp, self.house_text, 1, status_code=200)

    def test_404_for_non_exist_blog(self):
        resp = self.client.get(reverse('house_detail', args=[2]))
        self.assertEqual(resp.status_code, 404)


class MyHouseListViewTest(TestCase):
    number_of_entries = 10  # количество записей каждого вида для заполнения базы
    house_text = 'Описание квартиры'

    @classmethod
    def setUpTestData(cls):
        user_owner = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        user_not_owner1 = User.objects.create_user(username='len', password='111',
                                                   first_name='Елена', last_name='Смирнова')
        user_not_owner2 = User.objects.create_user(username='len2', password='111',
                                                   first_name='Елена', last_name='Смирнова')
        type_test = Type.objects.create(title='Тип', description='Тип жилья')
        rooms = Rooms.objects.create(number=1, description='Однокомнатная квартира')
        # список записей для трех авторов, у каждого по number_of_entries записей True и False
        cls.all_entries = cls.number_of_entries * 3 * 2  # всего записей
        cls.all_entries_owner = cls.number_of_entries * 2  # всего записей у каждого автора
        house_list = [House(owner=user,
                            title=f'{cls.house_text} {user.username} {num}',
                            type=type_test,
                            rooms=rooms,
                            description='text',
                            price=1e6,
                            actual=actual)
                      for user in (user_owner, user_not_owner1, user_not_owner2)
                      for num in range(cls.number_of_entries)
                      for actual in (True, False)]
        House.objects.bulk_create(house_list)

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get(reverse('my_house'))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("my_house")}')

    def test_view_url_exists_at_desired_location(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get('/realty/myadv/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('my_house'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('my_house'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_realty/my_house.html')

    def test_numbers_blog_in_list_view(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('my_house'))
        self.assertEqual(len(resp.context['house_list']), self.all_entries_owner)

    def test_context_in_blog_list_view(self):
        # Проверка, что выведено определенное количество записей и все записи принадлежат автору
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('my_house'))
        self.assertContains(resp, 'Описание квартиры nik',
                            self.all_entries_owner, status_code=200)
        self.assertNotContains(resp, 'len', status_code=200)


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class HouseCreateViewTest(TestCase):
    test_foto1 = SimpleUploadedFile('image1.jpg', b'111', content_type='image/jpeg')
    test_foto2 = SimpleUploadedFile('image2.jpg', b'222', content_type='image/jpeg')
    house_text = 'Описание квартиры'

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        type_test = Type.objects.create(title='Тип', description='Тип жилья')
        rooms = Rooms.objects.create(number=1, description='Однокомнатная квартира')

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get(reverse('house_create'))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("house_create")}')

    def test_view_url_exists_at_desired_location(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get('/realty/add/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_create'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_realty/house_create.html')

    def test_form_in_view(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_create'))
        self.assertIsNotNone(resp.context.get('form'), msg='Нет переменной шаблона: form')
        self.assertIsNotNone(resp.context.get('foto_form'), msg='Нет переменной шаблона: foto_form')
        self.assertIsNotNone(resp.context.get('user'))
        self.assertContains(resp, 'method="post"')

    def test_create_new_house(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        self.assertEqual(House.objects.all().count(), 0, msg='Должно быть 0 объектов')
        self.assertEqual(HouseFoto.objects.all().count(), 0, msg='Должно быть 0 объектов')
        self.client.post(reverse('house_create'), data={'title': 'Заголовок объявления',
                                                        'description': 'Описание квартиры',
                                                        'files': [self.test_foto1, self.test_foto2]})
        self.assertEqual(House.objects.all().count(), 1, msg='Должен быть 1 объект')
        self.assertEqual(HouseFoto.objects.all().count(), 2, msg='Должно быть 2 фото')

        new_house = House.objects.get(id=1)
        self.assertEqual(new_house.owner, user)
        self.assertEqual(new_house.title, 'Заголовок объявления')
        self.assertEqual(new_house.foto.count(), 2)

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class HouseEditViewTest(TestCase):
    test_foto_old = SimpleUploadedFile('image1.jpg', b'111', content_type='image/jpeg')
    test_foto_new = SimpleUploadedFile('image2.jpg', b'222', content_type='image/jpeg')
    house_text_old = 'Старое описание квартиры'
    house_text_new = 'Новое описание квартиры'

    @classmethod
    def setUpTestData(cls):
        owner = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        User.objects.create_user(username='len', password='111', first_name='Елена', last_name='Смирнова')
        type_test = Type.objects.create(title='Тип', description='Тип жилья')
        rooms = Rooms.objects.create(number=1, description='Однокомнатная квартира')
        house = House.objects.create(owner=owner, title='Объявление',
                                     type=type_test, rooms=rooms,
                                     description=cls.house_text_old,
                                     price=1e6, actual=True)
        HouseFoto.objects.create(house=house, foto=cls.test_foto_old)

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get(reverse('house_edit', args=[1]))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("house_edit", args=[1])}')

    def test_404_for_non_exist_house(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_edit', args=[2]))
        self.assertEqual(resp.status_code, 404)

    def test_access_for_non_owner(self):
        user = User.objects.get(id=2)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_edit', args=[1]))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get('/realty/1/edit/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_edit', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_edit', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_realty/house_edit.html')

    def test_form_in_view(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_edit', args=[1]))
        self.assertIsNotNone(resp.context.get('form'), msg='Нет переменной шаблона: form')
        self.assertIsNotNone(resp.context.get('foto_form'), msg='Нет переменной шаблона: foto_form')
        self.assertIsNotNone(resp.context.get('user'))
        self.assertContains(resp, 'method="post"')

    def test_edit_house(self):
        user = User.objects.get(id=1)
        house = House.objects.get(id=1)
        self.assertEqual(house.description, self.house_text_old)
        self.assertEqual(house.foto.count(), 1)
        self.client.force_login(user)
        self.client.post(reverse('house_edit', args=[1]), data={'title': 'Заголовок объявления',
                                                                'description': self.house_text_new,
                                                                'files': [self.test_foto_new]})
        house.refresh_from_db()
        self.assertEqual(house.description, self.house_text_new)
        self.assertEqual(house.foto.count(), 2)

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()

@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class HouseFotoDeleteViewTest(TestCase):
    test_foto = SimpleUploadedFile('image1.jpg', b'111', content_type='image/jpeg')

    @classmethod
    def setUpTestData(cls):
        owner = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        User.objects.create_user(username='len', password='111', first_name='Елена', last_name='Смирнова')
        type_test = Type.objects.create(title='Тип', description='Тип жилья')
        rooms = Rooms.objects.create(number=1, description='Однокомнатная квартира')
        house = House.objects.create(owner=owner, title='Объявление',
                                     type=type_test, rooms=rooms,
                                     description='Описание',
                                     price=1e6, actual=True)
        HouseFoto.objects.create(house=house, foto=cls.test_foto)

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get(reverse('delete_foto', args=[1]))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("delete_foto", args=[1])}')

    def test_404_for_non_exist_house(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('delete_foto', args=[2]))
        self.assertEqual(resp.status_code, 404)

    def test_access_for_non_owner(self):
        user = User.objects.get(id=2)
        self.client.force_login(user)
        resp = self.client.get(reverse('delete_foto', args=[1]))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get('/realty/foto/1/delete/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('delete_foto', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('delete_foto', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_realty/delete_foto.html')

    def test_delete_foto(self):
        user = User.objects.get(id=1)
        self.assertEqual(HouseFoto.objects.count(), 1)
        self.client.force_login(user)
        self.client.post(reverse('delete_foto', args=[1]), follow=True)
        self.assertEqual(HouseFoto.objects.count(), 0)

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()

@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class HouseDeleteViewTest(TestCase):
    test_foto = SimpleUploadedFile('image1.jpg', b'111', content_type='image/jpeg')

    @classmethod
    def setUpTestData(cls):
        owner = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        User.objects.create_user(username='len', password='111', first_name='Елена', last_name='Смирнова')
        type_test = Type.objects.create(title='Тип', description='Тип жилья')
        rooms = Rooms.objects.create(number=1, description='Однокомнатная квартира')
        house = House.objects.create(owner=owner, title='Объявление',
                                     type=type_test, rooms=rooms,
                                     description='Описание',
                                     price=1e6, actual=True)
        HouseFoto.objects.create(house=house, foto=cls.test_foto)

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get(reverse('house_delete', args=[1]))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("house_delete", args=[1])}')

    def test_404_for_non_exist_house(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_delete', args=[2]))
        self.assertEqual(resp.status_code, 404)

    def test_access_for_non_owner(self):
        user = User.objects.get(id=2)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_delete', args=[1]))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get('/realty/1/delete/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_delete', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        resp = self.client.get(reverse('house_delete', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_realty/house_delete.html')

    def test_delete_house(self):
        user = User.objects.get(id=1)
        self.assertEqual(House.objects.count(), 1)
        self.assertEqual(HouseFoto.objects.count(), 1)
        self.client.force_login(user)
        self.client.post(reverse('house_delete', args=[1]), follow=True)
        self.assertEqual(House.objects.count(), 0)
        self.assertEqual(HouseFoto.objects.count(), 0)

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()
