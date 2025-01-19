import docker

def launch_docker_container(image, name, ports=None, environment=None):
    client = docker.from_env()
    try:
        container = client.containers.run(
            image,
            name=name,
            ports=ports,
            environment=environment,
            detach=True
        )
        return f"Container launched successfully: {container.id}"
    except docker.errors.APIError as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def stop_docker_container(name):
    client = docker.from_env()
    try:
        container = client.containers.get(name)
        container.stop()
        return f"Container stopped: {name}"
    except docker.errors.NotFound:
        return f"Container not found: {name}"
    except Exception as e:
        return f"Error stopping container {name}: {e}"

def remove_docker_container(name):
    client = docker.from_env()
    try:
        container = client.containers.get(name)
        container.remove(force=True)  # Force removal if the container is running
        return f"Container removed: {name}"
    except docker.errors.NotFound:
        return f"Container not found: {name}"
    except Exception as e:
        return f"Error removing container {name}: {e}"

def is_container_running(name):
    client = docker.from_env()
    try:
        container = client.containers.get(name)
        return container.status == "running"
    except docker.errors.NotFound:
        return False
    except Exception as e:
        return f"Error checking container {name}: {e}"
