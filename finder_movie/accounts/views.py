from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, AuthenticationForm, UserProfileForm
from .models import UserProfile, FavoriteMovie

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
    favorite_movies = FavoriteMovie.objects.filter(user=request.user)

    return render(request, 'accounts/profile.html', {'favorite_movies': favorite_movies})

@login_required
def logout_view(request):
    logout(request)
    return redirect('movies_project:home')

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})

import logging

logger = logging.getLogger(__name__)

class AddToFavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        imdb_id = request.data.get('imdb_id')
        poster = request.data.get('poster')
        year = request.data.get('year')

        if not all([title, imdb_id, poster, year]):
            return Response({"error": "Все поля обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Received data: {request.data}")

        if FavoriteMovie.objects.filter(user=request.user, imdb_id=imdb_id).exists():
            return Response({"message": "Фильм уже в избранном"}, status=status.HTTP_400_BAD_REQUEST)

        FavoriteMovie.objects.create(
            user=request.user,
            title=title,
            imdb_id=imdb_id,
            poster=poster,
            year=year
        )

        return Response({"message": "Фильм добавлен в избранное"}, status=status.HTTP_201_CREATED)