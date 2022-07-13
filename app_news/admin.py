from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'actual']
    list_filter = ['date', 'actual']
    list_editable = ['actual']
    search_fields = ['title', 'text']
    date_hierarchy = 'date'
    # view_on_site = True
