# GibCasa GameServerSupervisor

# Setup 


* clone the repo
* create venv `python3 -m venv venv`
* activate `source venv/bin/activate`
* `pip install -r requirements.txt`
* will need docker running 
* Create admin user: `python manage.py createsuperuser` 
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py runserver`
* visit http://localhost:8000 for /public and 
  http://localhost:8000/admin/ to log in via the superuser credentials