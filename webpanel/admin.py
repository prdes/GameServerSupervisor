from django.contrib import admin, messages
from .models import Game, Server
from django import forms
from .widgets import PortMappingWidget

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = "__all__"
        widgets = {
            "port": PortMappingWidget(),
        }
    def clean_port(self):
        keys = self.data.getlist("port_key")
        values = self.data.getlist("port_value")

        try:
            return {
                k.strip(): int(v)
                for k, v in zip(keys, values)
                if k.strip() and v.strip()
            }
        except ValueError:
            raise forms.ValidationError("Port values must be integers.")
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
    form = ServerForm
    list_display = (
        'game', 'name', 'ip_address', 'get_ports_display', 'status', 'image', 'run_command', 'command_args'
    )
    search_fields = ('game__name', 'ip_address', 'port')
    list_filter = ('status', 'game')
    ordering = ('game', 'ip_address')
    actions = [stop_servers, remove_servers, launch_servers]

    readonly_fields = ('get_ports_display',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Sync status of all servers before rendering the admin list view."""
        queryset = super().get_queryset(request)
        for server in queryset:
            server.sync_status()
        return queryset

