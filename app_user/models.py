from pathlib import Path
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def path_for_avatar(instance, file_name):
    file_name = instance.user.username + Path(file_name).suffix
    path = Path('user') / 'foto' / file_name
    full_path = settings.MEDIA_ROOT / path
    if full_path.is_file():
        full_path.unlink()
    return path


class Profile(models.Model):
    """
    Расширение модели пользователя.
    """
    user = models.OneToOneField(User, verbose_name='пользователь', related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, verbose_name='Телефон', blank=True)
    contact = models.CharField(max_length=200, verbose_name='Контактные данные', blank=True)
    ava = models.ImageField(upload_to=path_for_avatar, blank=True, null=True, verbose_name='фото')

    def __str__(self):
        return f"'Профиль': {self.user.username}"

    def get_ava_url(self):
        url = '/media/user/000_no_foto.svg'
        if self.ava:
            url = self.ava.url
        return url

    def get_name(self):
        name = self.user.get_short_name()
        if not name:
            name = self.user.username
        return name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
