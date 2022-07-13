from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Profile


class UserChangeFormCustom(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {'email': 'e-mail'}


class ProfileForm(forms.ModelForm):

    phoneRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    class Meta:
        model = Profile
        fields = ('phone', 'contact')
