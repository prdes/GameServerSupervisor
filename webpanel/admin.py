from django.contrib import admin
from .models import Game, Server
from .utils import launch_docker_container, stop_docker_container, remove_docker_container

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')
    search_fields = ('name', 'genre')
    ordering = ('name',)

@admin.action(description='Launch Docker Container')
def launch_container(modeladmin, request, queryset):
    for server in queryset:
        container_name = f"{server.game.name}_{server.ip_address}_{server.port}"
        result = launch_docker_container(
            run_command=server.docker_run_command,
            name=container_name,
            image=server.docker_image,
            ports={f"{server.port}/tcp": server.port},
        )
        server.sync_status()
        modeladmin.message_user(request, f"Container launch result for {server}: {result}")

@admin.action(description='Stop Docker Container')
def stop_container(modeladmin, request, queryset):
    for server in queryset:
        container_name = f"{server.game.name}_{server.ip_address}_{server.port}"
        result = stop_docker_container(container_name)
        server.sync_status()
        modeladmin.message_user(request, f"Stop container result for {server}: {result}")

@admin.action(description='Remove Docker Container')
def remove_container(modeladmin, request, queryset):
    for server in queryset:
        container_name = f"{server.game.name}_{server.ip_address}_{server.port}"
        result = remove_docker_container(container_name)
        server.sync_status()
        modeladmin.message_user(request, f"Remove container result for {server}: {result}")

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('game', 'name', 'ip_address', 'port', 'status', 'docker_image', 'docker_run_command', 'command_args')
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
    search_fields = ('ip_address', 'game__name', 'docker_image')
    ordering = ('game', 'ip_address')
    actions = [launch_container, stop_container, remove_container]
