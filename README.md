# Django CoronaWatch API

**This is the main api of the project CoronaWatch for both Mobile and Web versions.**

**This API is written with Django 3.0.5 and Django Rest Framework 3.11.0.**

# Building

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv-2.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
```