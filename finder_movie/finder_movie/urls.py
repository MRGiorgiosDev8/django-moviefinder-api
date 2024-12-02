from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies_project.urls')),
    path('api/accounts/', include('accounts.urls')),
]
