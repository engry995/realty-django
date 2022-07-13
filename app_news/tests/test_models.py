from django.test import TestCase
from ..models import News


class NewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        News.objects.create(title='Новость', text='Текст новости')

    def test_fields_label(self):
        news = News.objects.get(id=1)
        self.assertEqual(news._meta.get_field('title').verbose_name, 'Заголовок')
        self.assertEqual(news._meta.get_field('text').verbose_name, 'Текст новости')
        self.assertEqual(news._meta.get_field('date').verbose_name, 'Дата новости')
        self.assertEqual(news._meta.get_field('actual').verbose_name, 'Активна')

    def str_method(self):
        news = News.objects.get(id=1)
        self.assertEqual(str(news), 'Новость: Новость')
