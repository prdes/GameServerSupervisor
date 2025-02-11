from django.shortcuts import render, get_object_or_404
from .models import Game, Server

def home(request):
    """Display the home page with links to other views."""
    games = Game.objects.all()  # Fetch all games
    return render(request, 'webpanel/home.html', {'games': games})

def games(request):
    games = Game.objects.all()
    return render(request, 'webpanel/games.html', {'games': games})

def game_detail(request, game_name):
    game = get_object_or_404(Game, id=game_name)
    return render(request, 'webpanel/game_detail.html', {'game': game})
