from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class CommonSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return ['about', 'contacts']

    def location(self, item):
        return reverse(item)
