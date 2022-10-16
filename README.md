
# CodeTest

Site for automatically evaluating programming exercises.

## Setup 

Create a config.json file (see config-sample.json).

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


## Information for Devs/Contributors

- Permissions are used in ```codetest/template/*_list.html```, ```codetest/template/*_form.html```, and ```codetest/template/*_detail.html``` to control which buttons/links each group can view.


