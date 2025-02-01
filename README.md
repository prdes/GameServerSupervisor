# GibCasa GameServerSupervisor

# Setup 


* clone the repo
* create venv `python3 -m venv venv`
* activate `source venv/bin/activate`
* `pip install -r requirements.txt`
* will need podman running 
* `python manage.py migrate`
* Create admin user: `python manage.py createsuperuser` 
* `python manage.py runserver`
* visit http://localhost:8000 for /public and 
  http://localhost:8000/admin/ to login via the superuser credentials