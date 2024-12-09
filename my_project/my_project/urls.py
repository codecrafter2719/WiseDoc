from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_auth.urls')),  # Include app-level URLs
    path('articles/', include('article_writing.urls')),
]
