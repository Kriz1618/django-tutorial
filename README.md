# Django Tutorial Project
Simple django project with some test api apps

## Clone
```
git clone git@github.com:Kriz1618/django-tutorial.git
```

## Create and activate a virtual environment
* `python -m venv env`
* `source env/bin/activate`


## Install modules
```
python -m pip install -r requirements.txt
```

## Start 
```
python manage.py runserver
```

## Run Tests
```
python manage.py test
```

## Format Code
```
autopep8 -i */*.py
```

## Steps
* Create folder `mkdir django-project && cd django-project`
* Create project `django-admin startproject tutorial .`
* Create an app `python manage.py startapp articles`
* Create a super user `python manage.py createsuperuser --email admin@example.com --username admin`
* Register app in the `settings.py` filed at `INSTALLED_APPS`
* Define the model in the file `articles/models.py`
* Create a new migration `python manage.py makemigrations articles`
* Excecute migration `python manage.py migrate articles`
* Define viewSets in the file `articles/views.py`
* Freeze modules in the requirements file `pip freeze >> requirements.txt`
* List endpoints `python manage.py show_urls`


