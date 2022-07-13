from django import forms


class FotoForm(forms.Form):
    files = forms.ImageField(
        required=False,
        label='Загрузить фото',
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
