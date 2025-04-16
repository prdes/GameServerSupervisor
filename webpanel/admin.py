from django.contrib import admin
from .models import Game, Server
from .utils import stop_pod_container, remove_pod_container
import podman
from django.contrib import messages


@admin.action(description="Launch selected servers")
def launch_servers(modeladmin, request, queryset):
    for server in queryset:
        result = server.launch_pod_container()
        messages.info(request, f"{server.name}: {result}")

@admin.action(description="Stop selected servers")
def stop_servers(modeladmin, request, queryset):
    for server in queryset:
        result = server.stop_pod_container()
        messages.info(request, f"{server.name}: {result}")

@admin.action(description="Remove selected servers")
def remove_servers(modeladmin, request, queryset):
    for server in queryset:
        result = server.remove_pod_container()
        messages.info(request, f"{server.name}: {result}")

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'thumbnail')
    search_fields = ('name', 'genre')
    ordering = ('name',)

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('game', 'name', 'ip_address', 'port', 'status', 'image', 'run_command', 'command_args')
    search_fields = ('game__name', 'ip_address', 'port')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Sync status of all servers before rendering the admin list view."""
        queryset = super().get_queryset(request)
        for server in queryset:
            server.sync_status()
        return queryset

    list_filter = ('status', 'game')
    search_fields = ('ip_address', 'game__name', 'image')
    ordering = ('game', 'ip_address')
    actions = [ stop_servers, remove_servers, launch_servers]
