from django.db import models
import docker

class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Server(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    docker_image = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')

    def __str__(self):
        return f"{self.game.name} Server at {self.ip_address}:{self.port}"

    def sync_status(self):
        """Check the real-time status of the Docker container and update the field."""
        client = docker.from_env()
        container_name = f"{self.game.name}_{self.ip_address}_{self.port}"
        try:
            container = client.containers.get(container_name)
            if container.status == "running":
                self.status = "online"
            else:
                self.status = "offline"
        except docker.errors.NotFound:
            self.status = "offline"
        except Exception as e:
            self.status = "offline"  # Fallback in case of unexpected errors
        self.save()
