from django.contrib.sitemaps import Sitemap
from .models import News


class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return News.objects.filter(actual=True)

    def lastmod(self, obj):
        return obj.date
