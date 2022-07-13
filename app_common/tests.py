from django.test import TestCase
from django.urls import reverse


class AboutViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/info/about/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_common/about.html')


class ContactsViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/info/contacts/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('contacts'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('contacts'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'app_common/contacts.html')

