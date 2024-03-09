# Task-Manager-API

A RESTful API for a simple task manager application using Django. 

## Description

The API allow users to perform basic CRUD operations on tasks and includes basic user authentication using JWT.


## Getting Started

### Dependencies

* Python 3
* Django
* Django Rest Framework
* djangorestframework-simplejwt (For JWT Authentication)
* drf-spectacular (For Swagger documentation)

### Live Demo

URL: [Task-Manager-API]()

### Installation

* Create Virtual Environment
``` 
python -m venv venv
```
* Activate Virtual Environment
``` 
python -m venv venv
```
* Install Packages
``` 
pip install -r requirements.txt
```
* Create DB tables
```
python manage.py migrate
```
* Load dummy data
```
python manage.py loaddata seed_data.json
```

* Run Server
```
python manage.py runserver
```
