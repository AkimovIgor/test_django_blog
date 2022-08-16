from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignUpForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'id': 'inputUsername',
            'placeholder': 'Имя пользователя',
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mt-2',
            'id': 'inputPassword',
            'placeholder': 'Пароль',
        })
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mt-2',
            'id': 'ReInputPassword',
            'placeholder': 'Пароль ещё раз',
        })
    )

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.save()
        return authenticate(**self.cleaned_data)

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']
        if password != confirm_password:
            raise forms.ValidationError(
                'Пароли не совпадают'
            )
