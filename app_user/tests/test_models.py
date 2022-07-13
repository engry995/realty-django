from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase, override_settings
from ..models import Profile
from django.conf import settings
import shutil


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_avatar = SimpleUploadedFile('avatar.jpg', b'fff', content_type='image/jpeg')
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')

    def test_create_profile(self):
        user = User.objects.get(id=1)
        profiles = Profile.objects.all()
        right_profiles = QuerySet(Profile(user=user))
        self.assertQuerysetEqual(profiles, right_profiles)

    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'пользователь')

    def test_ava_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('ava').verbose_name
        self.assertEqual(field_label, 'фото')

    def test_path_for_foto(self):
        profile = Profile.objects.get(id=1)
        profile.ava = self.test_avatar
        profile.save()
        path_foto = profile.ava.url
        self.assertEqual(path_foto, '/media/user/foto/nik.jpg')

    def test_get_name_method(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.get_name(), 'Иван')
        profile.user.first_name = ''
        profile.save()
        self.assertEqual(profile.get_name(), 'nik')


    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()
