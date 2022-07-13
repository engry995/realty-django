import shutil
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from ..models import Profile


class LoginTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/user/login/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_user/login.html')

    def test_redirect_for_authorized_user(self):
        # проверка перенаправления на главную страницу для авторизованного пользователя
        self.client.force_login(self.test_user)
        resp = self.client.get(reverse('login'))
        self.assertRedirects(resp, f'{reverse("main")}')

    def test_success_login(self):

        resp = self.client.post(reverse('login'), data={'username': 'nik', 'password': 111}, follow=True)
        self.assertIsNotNone(resp.context)
        self.assertIsNotNone(resp.context.get('user'), msg='Пользователь должен войти')
        self.assertTrue(resp.context['user'].is_authenticated, msg='Пользователь должен авторизоваться')


class LogoutTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.test_user)
        resp = self.client.get('/user/logout/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.test_user)
        resp = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на главную страницу для неавторизованного пользователя
        resp = self.client.get(reverse('logout'))
        self.assertRedirects(resp, f'{reverse("main")}')

    def test_success_logout(self):
        self.client.force_login(self.test_user)
        resp = self.client.get(reverse('logout'))
        self.assertIsNone(resp.context)


class UserRegistrationViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/user/reg/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('user_reg'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('user_reg'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_user/registration.html')

    def test_redirect_for_authorized_user(self):
        # проверка перенаправления на главную страницу для авторизованного пользователя
        self.client.force_login(User.objects.create_user('111'))
        resp = self.client.get(reverse('user_reg'))
        self.assertRedirects(resp, f'{reverse("main")}')

    def test_create_new_user(self):
        self.assertEqual(User.objects.all().count(), 0, msg='В базе не должно быть пользователей')
        self.client.post(reverse('user_reg'), data={'username': 'nik', 'password1': '111', 'password2': '111'})
        self.assertEqual(User.objects.all().count(), 1, msg='В базе должен быть создан один пользователь')


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class ProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_avatar = SimpleUploadedFile('avatar_old.jpg', b'000', content_type='image/jpeg')
        cls.new_avatar = SimpleUploadedFile('avatar_new.jpg', b'111', content_type='image/jpeg')
        cls.test_user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        # cls.test_profile = Profile.objects.create(user=cls.test_user, ava=cls.test_avatar)

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.test_user)
        resp = self.client.get('/user/profile/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.test_user)
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.test_user)
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_user/profile.html')

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на главную страницу для авторизованного пользователя
        resp = self.client.get(reverse('profile'))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("profile")}')

    def test_change_avatar(self):
        current_user = User.objects.get(id=1)
        # изначально аватар пустой
        self.assertFalse(current_user.profile.ava)
        # назначим аватар:
        current_user.profile.ava = self.test_avatar
        current_user.save()

        with current_user.profile.ava.open('r') as f:
            self.assertEqual(f.read(), '000')
        self.client.force_login(current_user)
        self.client.post(reverse('profile'), data={'ava': self.new_avatar})
        current_user.refresh_from_db()
        # содержимое файла изменилось на 111
        with current_user.profile.ava.open('r') as f:
            self.assertEqual(f.read(), '111')
        self.assertEqual(current_user.profile.ava.url, '/media/user/foto/nik.jpg')

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()
