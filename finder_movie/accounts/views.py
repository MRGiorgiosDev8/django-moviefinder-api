"""
Этот модуль содержит представления для управления учетными записями пользователей и их любимыми фильмами.

Функции:
- signup(request): Обрабатывает регистрацию нового пользователя.
- login_view(request): Обрабатывает вход пользователя в систему.
- profile_view(request): Отображает профиль пользователя с его любимыми фильмами.
- logout_view(request): Обрабатывает выход пользователя из системы.
- edit_profile(request): Обрабатывает редактирование профиля пользователя.
- remove_favorite(request, movie_id): Удаляет фильм из списка любимых фильмов пользователя.

Классы:
- AddToFavoritesAPIView(APIView): Обрабатывает добавление фильма в список любимых фильмов пользователя через API.

"""
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
    favorite_movies = FavoriteMovie.objects.filter(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'favorite_movies': favorite_movies
    })

class AddToFavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        imdb_id = request.data.get('imdb_id')
        poster = request.data.get('poster')
        year = request.data.get('year')
        imdb_rating = request.data.get('imdb_rating')
        genre = request.data.get('genre')
        plot = request.data.get('plot')
        actors = request.data.get('actors')
        movie_url = f"https://www.imdb.com/title/{imdb_id}/"

        FavoriteMovie.objects.create(
            user=request.user,
            title=title,
            imdb_id=imdb_id,
            poster=poster,
            year=year,
            imdb_rating=imdb_rating,
            genre=genre,
            plot=plot,
            actors=actors,
            movie_url = movie_url
        )

        return Response({"message": "Movie added to favorites"}, status=status.HTTP_201_CREATED)

@login_required
def remove_favorite(request, movie_id):
    try:
        favorite_movie = FavoriteMovie.objects.get(id=movie_id, user=request.user)
        favorite_movie.delete()
    except FavoriteMovie.DoesNotExist:
        pass

    return redirect('accounts:edit_profile')