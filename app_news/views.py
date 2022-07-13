from django.views import generic
from .models import News


class NewsList(generic.ListView):

    queryset = News.objects.filter(actual=True).order_by('-date')
    template_name = 'app_news/news_list.html'


class NewsDetail(generic.DetailView):

    model = News
    template_name = 'app_news/news_detail.html'