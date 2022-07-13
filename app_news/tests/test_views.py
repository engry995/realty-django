from django.test import TestCase
from django.urls import reverse
from ..models import News


class NewsListViewTest(TestCase):
    number_of_entries = 15  # количество записей для заполнения базы
    news_title = 'Заголовок новости '

    @classmethod
    def setUpTestData(cls):
        for num in range(cls.number_of_entries):
            News.objects.create(title=f'{cls.news_title} {num}.', text=f'Текст новости {num}')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/news/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('news_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('news_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_news/news_list.html')

    def test_numbers_blog_in_list_view(self):
        resp = self.client.get(reverse('news_list'))
        self.assertEqual(len(resp.context['news_list']), self.number_of_entries)

    def test_context_in_blog_list_view(self):
        # Проверка, что выведено определенное количество записей
        resp = self.client.get(reverse('news_list'))
        self.assertContains(resp, self.news_title, self.number_of_entries, status_code=200)


class NewsDetailViewTest(TestCase):

    news_text = 'Текст новости.'

    @classmethod
    def setUpTestData(cls):
        News.objects.create(title='Новость.', text=f'{cls.news_text}')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/news/1/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('news_view', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('news_view', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_news/news_detail.html')

    def test_context_blog_in_detail_view(self):
        resp = self.client.get(reverse('news_view', args=[1]))
        self.assertIsNotNone(resp.context.get('news'), msg='Нет переменной шаблона:')

    def test_context_in_blog_list_view(self):
        # Проверка, что выведена запись новости
        resp = self.client.get(reverse('news_view', args=[1]))
        self.assertContains(resp, self.news_text, 1, status_code=200)

    def test_404_for_non_exist_blog(self):
        resp = self.client.get(reverse('news_view', args=[2]))
        self.assertEqual(resp.status_code, 404)
