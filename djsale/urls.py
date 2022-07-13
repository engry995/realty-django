"""djsale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from app_news.sitemap import NewsSitemap
from app_realty.sitemap import HouseSitemap
from app_common.sitemap import CommonSitemap

sitemaps = {
    'news': NewsSitemap,
    'realty': HouseSitemap,
    'common': CommonSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('app_user.urls')),
    path('news/', include('app_news.urls')),
    path('rss/', include('app_rss.urls')),
    path('info/', include('app_common.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('app_realty.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
