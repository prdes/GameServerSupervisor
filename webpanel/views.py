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
    print(f"Looking for game: {game_name}")
    game = get_object_or_404(Game, name=game_name)
    servers = Server.objects.filter(game=game)
    for server in servers:
        server.sync_status()
    dormant_servers = servers.filter(status='offline')
    active_servers = servers.filter(status='online') 
    return render(request, 'webpanel/game_detail.html', {'game': game,
                'active_servers': active_servers, 'dormant_servers': dormant_servers})

# def game_detail(request, pk):
#     game = get_object_or_404(Game, pk=pk)
#     return render(request, 'webpanel/game_detail.html', {'game': game})

# def active_servers_view(request):
#     """Fetch and display all active servers."""
#     # Sync server status before fetching
#     servers = Server.objects.all()
#     for server in servers:
#         server.sync_status()
    
#     # Fetch only servers with status 'online'
#     active_servers = Server.objects.filter(status='online')
    
#     return render(request, 'webpanel/active_servers.html', {'servers': active_servers})

# def game_servers_view(request, game_name):
#     """Fetch and display active servers for a specific game."""
#     game = get_object_or_404(Game, name=game_name)

#     # Sync server status before fetching
#     servers = Server.objects.filter(game=game)
#     for server in servers:
#         server.sync_status()

#     # Fetch only active servers for the game
#     active_servers = servers.filter(status='online')

#     return render(request, 'webpanel/game_servers.html', {'game': game, 'servers': active_servers})