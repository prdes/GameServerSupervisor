from django.shortcuts import render, get_object_or_404
from .models import Game, Server
from .utils import a2s_query
import logging

logger = logging.getLogger(__name__)

PROTOCOL_FUNCTION_MAP = {
    'a2s': a2s_query,
    # Add other protocols here -> 'quake2': query_quake2, etc.
}


def home(request):
    """Display the home page with links to other views."""
    games = Game.objects.all()  # Fetch all games
    return render(request, 'webpanel/home.html', {'games': games})

def games(request):
    games = Game.objects.all()
    return render(request, 'webpanel/games.html', {'games': games})

def game_detail(request, game_name):
    logger.info(f"Accessing game detail for: {game_name}") # Use logger.info or logger.debug
    game = get_object_or_404(Game, name__iexact=game_name) # Use iexact for case-insensitivity

    query_protocol = getattr(game, 'query_protocol', 'none') # Safely get protocol
    query_function = PROTOCOL_FUNCTION_MAP.get(query_protocol)
    default_port_key = getattr(game, 'default_query_port_key', None) # Safely get port key

    if not query_function:
        logger.debug(f"Live query disabled for game '{game.name}' (protocol '{query_protocol}' not mapped or 'none').")
    elif not default_port_key:
         logger.warning(f"Live query configured for '{game.name}' (protocol '{query_protocol}') but 'Default query port key' is not set in Game model.")
    else:
         logger.debug(f"Live query configured for '{game.name}': Protocol='{query_protocol}', Port Key='{default_port_key}'")
    servers_queryset = Server.objects.filter(game=game)

    active_server_list = []
    dormant_server_list = []

    for server in servers_queryset:
        server.sync_status()  
        server.live_stats = None  

        if server.status == 'online' and a2s_query and default_port_key:
            logger.debug(f"Server '{server.name}' is online, attempting query using protocol '{query_protocol}'.")

            query_port_host = None
            port_keys_to_try = [default_port_key]
            if '/' in default_port_key:
                 port_keys_to_try.append(default_port_key.split('/')[0]) # Try without /udp suffix

            for key in port_keys_to_try:
                 if isinstance(server.port, dict) and key in server.port: # Check if server.port is a dict
                     try:
                         query_port_host = int(server.port[key])
                         logger.debug(f"Found host query port {query_port_host} using key '{key}'.")
                         break
                     except (ValueError, TypeError):
                        logger.warning(f"Invalid port value '{server.port[key]}' for key '{key}' in server '{server.name}'.")
                        query_port_host = None

            if query_port_host is None:
                logger.warning(f"Could not find host port for key '{default_port_key}' (or fallback) in server '{server.name}'. Port data: {server.port}")

            ip_to_query = server.ip_address
            if not ip_to_query or ip_to_query in ["0.0.0.0", "::"]:
                ip_to_query = "127.0.0.1" # Default to localhost
                logger.debug(f"Using IP {ip_to_query} for query.")

            if ip_to_query and query_port_host is not None:
                try:
                    logger.info(f"Querying {game.name} server '{server.name}' at {ip_to_query}:{query_port_host}")
                    server.live_stats = a2s_query(ip=ip_to_query, port=query_port_host) # Call the mapped function
                    if server.live_stats:
                         logger.info(f"Query successful for '{server.name}'.") # Add more detail if needed
                    else:
                         logger.warning(f"Query returned no data for '{server.name}'.")
                except Exception as e:
                    logger.error(f"Error querying server '{server.name}': {e}", exc_info=True)
                    server.live_stats = None # Ensure it's None on error
            else:
                logger.warning(f"Skipping query for '{server.name}': Missing IP or Host Port.")

        if server.status == 'online':
            active_server_list.append(server)
        else:
            dormant_server_list.append(server)

    return render(request, 'webpanel/game_detail.html', {
        'game': game,
        'active_servers': active_server_list, # Use the list we built
        'dormant_servers': dormant_server_list # Use the list we built
    })