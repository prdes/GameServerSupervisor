from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.games, name='games')
    # path('<int:pk>/', views.game_detail, name='game_detail'),
    # path('active-servers/', views.active_servers_view, name='active-servers'),
    # path('games/<str:game_name>/', views.game_servers_view, name='game-servers'),
]