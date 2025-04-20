from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.games, name='games'),
    path('games/<str:game_name>/', views.game_detail, name='game_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
