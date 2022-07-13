from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Type, Rooms, House, HouseFoto


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('number', 'description')
    ordering = ('number',)


class FotoInline(admin.TabularInline):
    model = HouseFoto
    readonly_fields = ('preview',)
    fields = ('foto', 'preview')
    extra = 1

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.foto.url}" style="max-height: 150px;">')

    preview.short_description = 'Просмотр'


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    list_display = ('title', 'price', 'actual')
    list_filter = ('owner', 'type', 'rooms')
    search_fields = ['title', 'description']
    inlines = [FotoInline, ]


@admin.register(HouseFoto)
class HouseFotoAdmin(admin.ModelAdmin):

    list_filter = ('house', )
    readonly_fields = ('preview',)
    fields = ('house', 'foto', 'preview')

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.foto.url}" style="max-height: 200px;">')

    preview.short_description = 'Просмотр'
