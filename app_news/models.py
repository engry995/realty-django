from django.urls import reverse
from django.utils import timezone
from django.db import models


class News(models.Model):

    title = models.CharField(max_length=200, db_index=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст новости')
    date = models.DateTimeField(verbose_name='Дата новости', default=timezone.now)
    actual = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self) -> str:
        return f'Новость: {self.title}'

    def get_absolute_url(self):
        return reverse('news_view', args=[self.pk])

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ['-date']
