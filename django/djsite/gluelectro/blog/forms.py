import string
from transliterate import translit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].required = False

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'body': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'tags': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'title': 'Заголовок',
            'slug': 'Слаг',
            'body': 'Текст поста',
            'tags': 'Тэги',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 120:
            raise ValidationError('Длина превышает максимльное количество символов')
        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Ник', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """
        Пользовательский валидатор email: в базе все адреса должны быть уникальны
        """
        new_email = self.cleaned_data['email']
        email_is_in_db = User.objects.filter(email=new_email).exists()
        if email_is_in_db:
            raise ValidationError('Пользователь с такой почтой уже зарегистрирован')
        return new_email


class VerificationCodeForm(forms.ModelForm):
    verification_code = forms.CharField(label='Код верификации', max_length=5)
    is_error = False

    class Meta:
        model = User
        fields = ('verification_code',)

    def clean(self):
        if self.is_error:
            self.add_error('verification_code', 'Код введён неверно')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='Ваш комментарий', max_length=155)

    class Meta:
        model = Comment
        fields = ['body']
