from django.contrib.syndication.views import Feed
from django.urls import reverse
from app_news.models import News
from app_realty.models import House
from django.utils import timezone


class NewsFeed(Feed):

    title = 'Новости сайта объявлений о продаже жилья'
    link = '/rss/'
    description = 'Лента новостей сайта объявлений о продаже жилья.'

    def feed_url(self):
        return reverse('news_feed')

    def items(self):
        return News.objects.filter(actual=True, date__lte=timezone.now()).order_by('-date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_pubdate(self, item):
        return item.date


class HouseFeed(Feed):

    title = 'Лента новых объявлений о продаже жилья'
    link = '/rss/'
    description = 'Здесь появляются все опубликованные объявления'

    def items(self):
        return House.objects.filter(actual=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
