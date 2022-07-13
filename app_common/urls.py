from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='app_common/about.html'), name='about'),
    path('contacts/', TemplateView.as_view(template_name='app_common/contacts.html'), name='contacts'),
]
