# Task-Manager-API

A RESTful API for a simple task manager application using Django.

## Description

The API allow users to perform basic CRUD operations on tasks and includes basic user authentication using JWT.

-   All users can view all task or a specific task.
-   Normal users can create or update tasks.
-   Staff users can create, update, or delete tasks.

## Live Demo

Swagger UI URL: [Task-Manager-API](https://abhinav9a.pythonanywhere.com/api/schema/swagger-ui/)

Admin Panel: [Admin Panel](https://abhinav9a.pythonanywhere.com/admin/)

## Getting Started

### Dependencies

-   Python 3
-   Django
-   Django Rest Framework
-   djangorestframework-simplejwt (For JWT Authentication)
-   drf-spectacular (For Swagger documentation)

### Installation

-   Create Virtual Environment

```
python -m venv venv
```

-   Activate Virtual Environment

```
python -m venv venv
```

-   Install Packages

```
pip install -r requirements.txt
```

-   Create DB tables

```
python manage.py migrate
```

-   Load dummy data

| Username | Password      | User Type   |
| -------- | ------------- | ----------- |
| admin    | adminpassword | superuser   |
| staff    | staffpassword | staff user  |
| test     | testpassword  | Normal user |

```
python manage.py loaddata seed_data.json
```

-   Run Server

```
python manage.py runserver
```

## Test

```
python manage.py test api.tests
```
