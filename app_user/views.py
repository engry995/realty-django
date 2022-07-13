from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import F
from .forms import UserChangeFormCustom, ProfileForm


def user_registration(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main'))

    if request.method != 'POST':
        return render(request, 'app_user/registration.html', {'form': UserCreationForm()})

    new_user = UserCreationForm(request.POST)
    if new_user.is_valid():
        new_user = new_user.save()
        login(request, new_user)
        return HttpResponseRedirect(reverse('profile'))
    else:
        return render(request, 'app_user/registration.html', {'form': new_user})


@login_required
def profile_view(request: HttpRequest):
    user = request.user
    message = None

    if request.method == 'POST':
        user_form = UserChangeFormCustom(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            avatar = request.FILES.get('ava')
            if avatar:
                user.profile.ava = avatar
            user_form.save()
            message = 'Изменения успешно внесены.'
        else:
            message = 'Ошибка, проверьте введенные данные!'
    else:
        user_form = UserChangeFormCustom(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    return render(request, 'app_user/profile.html', {'form': user_form,
                                                     'profile_form': profile_form,
                                                     'message': message})
