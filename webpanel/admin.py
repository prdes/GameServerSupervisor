from django.contrib import admin
from .models import Game, Server
from .utils import launch_pod_container, stop_pod_container, remove_pod_container
import podman

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')
    search_fields = ('name', 'genre')
    ordering = ('name',)

@admin.action(description='Launch Container')
def launch_container(modeladmin, request, queryset):
    client = podman.PodmanClient(base_url="unix:///run/user/1000/podman/podman.sock")
    for server in queryset:
        container_name = f"{server.game.name}_{server.ip_address}_{server.port}"
        try:
            # Ensure the command is passed as a list of strings
            command = server.get_podman_run_command().split() if server.run_command else []
            container = client.containers.run(
                server.image,
                detach=True,
                name=container_name,
                command=command,
                ports={f"{server.port}/tcp": server.port},
                remove=True,  # Automatically remove on stop
            )
            server.sync_status()
            modeladmin.message_user(request, f"Container launched: {container.id}")
        except Exception as e:
            modeladmin.message_user(request, f"Failed to launch {server}: {e}", level="error")

@admin.action(description='Stop Container')
def stop_container(modeladmin, request, queryset):
    for server in queryset:
        container_name = f"{server.game.name}_{server.ip_address}_{server.port}"
        result = stop_pod_container(container_name)
        server.sync_status()
        modeladmin.message_user(request, f"Stop container result for {server}: {result}")

@admin.action(description='Remove Container')
def remove_container(modeladmin, request, queryset):
    for server in queryset:
        container_name = f"{server.game.name}_{server.ip_address}_{server.port}"
        result = remove_pod_container(container_name)
        server.sync_status()
        modeladmin.message_user(request, f"Remove container result for {server}: {result}")

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
    actions = [launch_container, stop_container, remove_container]
