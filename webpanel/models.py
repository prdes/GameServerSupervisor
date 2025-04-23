from django.db import models
import podman
import shlex
import re
from typing import Optional,List

class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='game_thumbnails/', null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Server(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    last_log = models.TextField(blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True)
    port = models.JSONField(default=dict, blank=True)
    image = models.CharField(max_length=200, null=True)
    run_command = models.CharField(max_length=500, blank=True, null=True) 
    command_args = models.TextField(blank=True, null=True)
    container_id = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')

    def __str__(self)-> str:
        return f"{self.game.name} Server at {self.ip_address}:{self.port}"

    @property
    def safe_name(self) -> str:
        """Return a container-safe version of the server name"""
        return re.sub(r'[^a-zA-Z0-9_.-]', '_', self.name)

    def _log_error(self, msg):
        self.last_log = msg
        self.save(update_fields=["status", "last_log"])
    def _get_podman_client(self) -> podman.PodmanClient:
        """Get a configured Podman client instance."""
        return podman.PodmanClient(base_url="unix:///run/user/1000/podman/podman.sock")

    def sync_status(self) -> None:
        """Check the real-time status of the container and update the field."""
        try:
            container = self._get_podman_client().containers.get(self.safe_name)
            if container.status == "running":
                self.status = "online"
            else:
                self.status = "offline"
        except podman.errors.NotFound:
            self.status = "offline"
        except Exception as e:
            self.status = "offline"
        self.save()

    def get_ports_display(self):
        return ", ".join(f"{k}→{v}" for k, v in self.port.items())
    get_ports_display.short_description = "Ports"  # display name in admin


    def launch_pod_container(self) -> str:
        try:
            port_bindings = {
                container_port: ('0.0.0.0', host_port)
                for container_port, host_port in self.port.items()
            }

            container = self._get_podman_client().containers.create(
                name=self.safe_name,
                image=self.image,
                ports=port_bindings,
                command=shlex.split(self.run_command),
                detach=True,
            )
            container.start()
            self.container_id = container.id
            self.last_log = f"Launched container {container.id}"
            self.sync_status()
            self.save()
            return f"Container launched successfully: {container.id}"
        except podman.errors.APIError as e:
            self.last_log = f"API Error: {str(e)}"
            self.save()
            return f"API Error: {e}"
        except Exception as e:
            self.last_log = f"Error: {str(e)}"
            self.save()
            return f"Error: {e}"

    def stop_pod_container(self) -> str:
        try:
            container = self._get_podman_client().containers.get(self.safe_name)
            container.stop()
            self.status = "offline"
            self.last_log = f"Stopped container {container.id}"
            self.sync_status()
            self.save()
            return f"Container stopped successfully: {container.id}"
        except podman.errors.NotFound:
            self.last_log = f"Container '{self.safe_name}' not found"
            self.save()
            return f"Error: Container '{self.safe_name}' not found"
        except Exception as e:
            self.last_log = f"Error stopping container: {str(e)}"
            self.save()
            return f"Error: {e}"

    def remove_pod_container(self) -> str:
        try:
            container = self._get_podman_client().containers.get(self.safe_name)
            container.remove(force=True)
            self.status = "offline"
            self.container_id = None
            self.last_log = f"Removed container {self.safe_name}"
            self.sync_status()
            self.save()
            return f"Container removed successfully: {self.safe_name}"
        except podman.errors.NotFound:
            self.last_log = f"Container '{self.safe_name}' not found"
            self.save()
            return f"Error: Container '{self.safe_name}' not found"
        except Exception as e:
            self.last_log = f"Error removing container: {str(e)}"
            self.save()
            return f"Error: {e}"