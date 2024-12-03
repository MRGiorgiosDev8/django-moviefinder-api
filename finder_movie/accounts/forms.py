from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as DefaultAuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class AuthenticationForm(DefaultAuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='remember me')

    class Meta:
        model = CustomUser
        fields = ['username', 'password']