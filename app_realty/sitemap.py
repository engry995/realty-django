from django.contrib.sitemaps import Sitemap
from .models import House


class HouseSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return House.objects.filter(actual=True)
