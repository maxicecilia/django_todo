[![Build Status](https://travis-ci.org/maxicecilia/django_todo.svg?branch=master)](https://travis-ci.org/maxicecilia/django_todo)

Django To-Do
===========

Simple django application built to work as example of what Django can do for the life of a web developer.

This application defines and displays the basics functionalities needed to create and manage tasks.


Requirements
----------------
* Django==1.7


Installation
----------------
*Note: please setup a [virtualenv](https://virtualenv.pypa.io/en/latest/) before installing.*
```
# clone repo
$ git clone git@github.com:maxicecilia/django_todo.git
# install dependencies
$ pip install -r requirements.txt
# run migrations (using sqlite by default)
$ python manage.py migrate
# Check that all tests pass
$ python manage.py test
# Run the application
$ django-admin.py runserver 0.0.0.0:8000
```