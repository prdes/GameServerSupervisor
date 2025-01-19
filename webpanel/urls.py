from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('<int:pk>/', views.game_detail, name='game_detail'),
    path('active-servers/', views.active_servers_view, name='active-servers'),
    path('games/<str:game_name>/', views.game_servers_view, name='game-servers'),
]