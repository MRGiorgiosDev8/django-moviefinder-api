from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as DefaultAuthenticationForm
from .models import CustomUser, UserProfile, FavoriteMovie

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False, label='Avatar (Optional)')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        if self.cleaned_data.get('avatar'):
            user.profile.avatar = self.cleaned_data.get('avatar')
            user.profile.save()
        return user

class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, label='Upload Avatar')
    birth_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    location = forms.CharField(required=False, max_length=100)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'birth_date', 'location')

class AuthenticationForm(DefaultAuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='remember me')

    class Meta:
        model = CustomUser
        fields = ['username', 'password']