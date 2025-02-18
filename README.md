# GibCasa GameServerSupervisor

## Table of Contents
- [Installation using venv](#installation-using-venv)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Installation using Podman](#installation-using-podman)
  - [Prerequisites](#prerequisites-1)
  - [Installation](#installation-1)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation using venv

### Prerequisites

Python 3.10 or above

### Installation

1. Clone the repository:
```bash
  git clone https://git.com.de/GibCasa/GameServerSupervisor
```
2. Create a virtual environment in Python:
```bash
  python -m venv venv
```
3. Activate the virtual environment:
```bash
  source venv/bin/activate
```
4. Install dependencies:
```bash
  pip install -r requirements.txt
```
5. Run tests:
```bash
  ./manage.py test
```
6. Run migrations:
```bash
  ./manage.py migrate
```
7. Create admin user:
```bash
  ./manage.py createsuperuser
```
8. Run server:
```bash
  ./manage.py runserver
```
## Installation using Podman

### Prerequisites

Podman

### Installation

1. Clone the repository:
```bash
  git clone https://git.com.de/GibCasa/GameServerSupervisor
```
2. Build the image:
```bash
  podman build . -t supervisor-image
```
3. Run a container in an interactive shell:
```bash
  podman run -it --network=host localhost/supervisor-image sh
```
4. Run tests:
```bash
  ./manage.py test
```
5. Run migrations:
```bash
  ./manage.py migrate
```
6. Create admin user:
```bash
  ./manage.py createsuperuser
```
7. Run server:
```bash
  ./manage.py runserver
```

## Usage

* Visit http://localhost:8000 for /public and 
  http://localhost:8000/admin/ to login via the superuser credentials

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.

## License

This project is licensed under the [AGPL](https://www.gnu.org/licenses/agpl-3.0.html).

