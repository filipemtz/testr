
# Testr

Site for automatically evaluating programming exercises.

## Setup 

Create a config.json file (see config-sample.json). For using PostgreSQL, refer to
the respective section below.

Install docker by following the instructions in the [documentation](https://docs.docker.com/engine/install/).

Build the docker image used by the autojudge: 

```
# linux
sh ./data/docker_imgs/create_docker_image.sh

# windows
.\data\docker_imgs\create_docker_image.sh
```

Install python requirements:

```
python -m pip install -r requirements.txt 
```

Setup the system database. 

```
python manage.py migrate
```

Create user for the admin page (acessible via /admin).

```
python manage.py createsuperuser
```

Create groups and assign permissions.

```
python manage.py setperms permissions.json
```

That's it. Use the command below to run the server and follow the URL presented 
in the terminal to start using the system. 

```
python manage.py runserver
```

Use the following commando to start the autojudge system. It will evaluate all
submissions that were not evaluated yet and then wait for new submissions. If 
the autojudge is not run, users will not receive the result of their submissions.

```
python manage.py judge
```

**Observation:** Use ```--help```  to check the options available in the autojudge system, e.g., re-evaluate all submissions, keep submitted files saved on disk, etc.


## Set-up with PostgreSQL

Follow the instructions in this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04) to configure
postgresql to be used with django. The typical commands are given below:

```
sudo -u postgres psql
CREATE DATABASE testr;
CREATE USER testr_user WITH PASSWORD 'password';
ALTER ROLE testr_user SET client_encoding TO 'utf8';
ALTER ROLE testr_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE testr_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE testr TO testr_user;
\q
```

Add the database connection information in config.json.

## Information for Devs/Contributors

- Permissions are used in ```testr/template/*_list.html```, ```testr/template/*_form.html```, and ```testr/template/*_detail.html``` to control which buttons/links each group can view.

- [Django documentation](https://docs.djangoproject.com/en/4.1/).

- [Django tutorial by Mozilla](https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Django).

- [Tutorial on how to use docker to run applications](https://phoenixnap.com/kb/docker-run-command-with-examples).

- [See this stackoverflow discussion for different ways of running docker from python](https://stackoverflow.com/questions/44862100/need-to-run-docker-run-command-inside-python-script).