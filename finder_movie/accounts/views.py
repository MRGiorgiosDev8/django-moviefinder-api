from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, AuthenticationForm
from .models import UserProfile


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': user_profile})


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')