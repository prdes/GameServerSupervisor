# GibCasa GameServerSupervisor

## Prerequisites

Python 3.10 or above

## Installation 

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
5. Run migrations:
```bash
  python manage.py migrate
```
6. Create admin user:
```bash
  python manage.py createsuperuser
```
7. Run server:
```bash
  python manage.py runserver
```
* visit http://localhost:8000 for /public and 
  http://localhost:8000/admin/ to login via the superuser credentials

