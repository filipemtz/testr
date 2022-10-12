
# CodeTest

Site for automatically evaluating programming exercises.

## Setup 

Install requirements.

```
python -m pip install -r requirements.txt 
```

Setup the database. 

```
python manage.py migrate
```

Create user for the admin page (acessible via /admin).

```
python manage.py createsuperuser
```

That's it. Just run the server and follow the URL presented in the terminal
to start using the system.

```
python manage.py runserver
```




