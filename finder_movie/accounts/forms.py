from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as DefaultAuthenticationForm
from .models import CustomUser, UserProfile, FavoriteMovie

class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания новых пользователей. Включает все необходимые
    поля, плюс повторный пароль и необязательный аватар.
    """
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False, label='Аватар (необязательно)')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

    def save(self, commit=True):
        """
        Сохраняет предоставленный пароль в зашифрованном формате и обрабатывает аватар.

        :param commit: Сохранять ли экземпляр после создания.
        :return: Созданный экземпляр пользователя.
        """
        user = super().save(commit=False)
        if commit:
            user.save()

        if self.cleaned_data.get('avatar'):
            user.profile.avatar = self.cleaned_data.get('avatar')
            user.profile.save()
        return user

class UserProfileForm(forms.ModelForm):
    """
    Форма для обновления профилей пользователей. Включает поля для аватара,
    даты рождения и местоположения.
    """
    avatar = forms.ImageField(required=False, label='Загрузить аватар')
    birth_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    location = forms.CharField(required=False, max_length=100)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'birth_date', 'location')

class AuthenticationForm(DefaultAuthenticationForm):
    """
    Форма для аутентификации пользователей. Включает флажок 'запомнить меня'.
    """
    remember_me = forms.BooleanField(required=False, label='запомнить меня')

    class Meta:
        model = CustomUser
        fields = ['username', 'password']