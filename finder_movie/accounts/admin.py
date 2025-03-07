from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, FavoriteMovie

class CustomUserAdmin(UserAdmin):
    """
    Админ-панель для модели CustomUser.
    """
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        """
        Получает встроенные экземпляры для модели UserProfile.
        """
        if obj:
            return [UserProfileInline(self.model, self.admin_site)]
        return []


class UserProfileInline(admin.StackedInline):
    """
    Встроенная модель для профиля пользователя.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('avatar', 'birth_date', 'location')
    readonly_fields = ('avatar',)

class UserProfileAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели UserProfile.
    """
    model = UserProfile
    list_display = ('user', 'avatar', 'birth_date', 'location')
    search_fields = ('user__username', 'location')
    list_filter = ('birth_date',)

class FavoriteMovieAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели FavoriteMovie.
    """
    model = FavoriteMovie
    list_display = ('user', 'title', 'year', 'imdb_id', 'poster', 'imdb_rating', 'genre', 'actors', 'movie_url')
    search_fields = ('title', 'imdb_id', 'genre', 'actors', 'movie_url')
    list_filter = ('year', 'user', 'genre')
    readonly_fields = ('imdb_id',)

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'year', 'imdb_id', 'poster')
        }),
        ('Дополнительная информация', {
            'fields': ('imdb_rating', 'genre', 'plot', 'actors', 'movie_url')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FavoriteMovie, FavoriteMovieAdmin)