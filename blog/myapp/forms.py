from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, hashers
from .models import Comment


class SignUpForm(forms.Form):
    """Форма регистрации"""

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


class SignInForm(forms.Form):
    """Форма входа"""

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
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'id': 'inputPassword',
            'placeholder': 'Пароль',
        })
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            hashers.check_password(password, user.password)
        except forms.ValidationError as error:
            self.add_error('password', error)
        except:
            self.add_error('password', Exception('Неверный логин/пароль'))
        return password


class FeedBackForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': 'Ваше имя',
        })
    )

    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'Ваша почта',
        })
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': 'Тема',
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control md-textarea',
            'id': 'message',
            'rows': 2,
            'placeholder': 'Ваше сообщение'
        })
    )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            })
        }
