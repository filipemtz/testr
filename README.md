
# Testr

Site for automatically evaluating programming exercises.

## Setup 

Create a config.json file (see config-sample.json). For using PostgreSQL, refer to
the respective section below.

Install docker by following the instructions in the [documentation](https://docs.docker.com/engine/install). The common commands are given in the specific section below.

Build the docker image used by the autojudge: 

```
# linux
cd ./data/docker_imgs/base/ && sudo sh ./create_base_docker_image.sh && cd ../../../

# windows
cd .\data\docker_imgs\base
.\create_base_docker_image.sh
cd ../../../
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

To allow django to be accessed from a different computer, add the server computer IP to ALLOWED_HOSTS, and run the server as follows: 

```
python manage.py runserver 0.0.0.0:8000
```

Use this strategy during development, but refer to [django documentation](https://docs.djangoproject.com/en/4.1/howto/deployment/) to learn more about how to deploy an application.

## Set-up Docker on Ubuntu

```
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Receiving a GPG error when running the second apt-get update? Your default umask may be incorrectly configured, preventing detection of the repository public key file. Try granting read permission for the Docker public key file before updating the package index:

```
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update
```

Verify that the Docker Engine installation is successful by running the hello-world image:

```
sudo docker run hello-world
```

To allow non-root users to use docker, create a docker group and add the user to the group. Keep in mind that [the docker group grants privileges equivalent to the root user](https://docs.docker.com/engine/install/linux-postinstall/).

```
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker 
```

## Set-up with PostgreSQL

Follow the instructions in this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04).

To install postgre in ubuntu, use: 

```
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
```

To configure postgresql to be used with django, use:

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