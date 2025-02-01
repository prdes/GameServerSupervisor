import podman

def launch_pod_container(image, run_command, name, ports):
    client = podman.PodmanClient(base_url="unix:///run/user/1000/podman/podman.sock")
    try:
        container = client.containers.create(
            name=name,
            image=image,
            # ports=ports,
            command=run_command,
            detach=True,
            network_mode='host'
        )
        container.start()
        return f"Container launched successfully: {container.id}"
    except podman.errors.APIError as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def stop_pod_container(name):
    client = podman.PodmanClient(base_url="unix:///run/user/1000/podman/podman.sock")
    try:
        container = client.containers.get(name)
        container.stop()
        return f"Container stopped: {name}"
    except podman.errors.NotFound:
        return f"Container not found: {name}"
    except Exception as e:
        return f"Error stopping container {name}: {e}"

def remove_pod_container(name):
    client = podman.PodmanClient(base_url="unix:///run/user/1000/podman/podman.sock")
    try:
        container = client.containers.get(name)
        container.remove(force=True)  # Force removal if the container is running
        return f"Container removed: {name}"
    except podman.errors.NotFound:
        return f"Container not found: {name}"
    except Exception as e:
        return f"Error removing container {name}: {e}"

def is_container_running(name):
    client = podman.PodmanClient(base_url="unix:///run/user/1000/podman/podman.sock")
    try:
        container = client.containers.get(name)
        return container.status == "running"
    except podman.errors.NotFound:
        return False
    except Exception as e:
        return f"Error checking container {name}: {e}"
