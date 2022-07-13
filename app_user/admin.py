from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from .models import Profile


class ProfileInline(admin.TabularInline):

    model = Profile
    can_delete = False
    readonly_fields = ('preview', )
    fields = ('ava', 'preview', 'phone', 'contact')

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.get_ava_url()}" style="max-height: 200px;">')

    preview.short_description = 'Просмотр фото'


class UserAdmin(BaseUserAdmin):

    list_display = ('username', 'full_name', 'email', 'is_superuser')
    inlines = (ProfileInline, )

    def full_name(self, user):
        return user.get_full_name()

    full_name.short_description = 'Полное имя'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
