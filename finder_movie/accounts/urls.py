from django.urls import path
from .views import signup, login_view, profile_view, logout_view, edit_profile, AddToFavoritesAPIView, remove_favorite

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('add-to-favorites/', AddToFavoritesAPIView.as_view(), name='add_to_favorites'),
    path('remove_favorite/<int:movie_id>/', remove_favorite, name='remove_favorite'),
]