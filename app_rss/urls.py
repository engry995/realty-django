from django.urls import path
from django.views.generic import TemplateView

from .feeds import NewsFeed, HouseFeed

urlpatterns = [
    path('news/', NewsFeed(), name='news_feed'),
    path('realty/', HouseFeed(), name='house_feed'),
    path('channels', TemplateView.as_view(template_name='app_rss/rss_list.html'), name='rss_list'),
]
