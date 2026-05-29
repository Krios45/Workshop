# Workshop Management

Django project for managing workshop assets, bookings, inventory, and maintenance.

## Requirements

- Python 3.10+
- Django 5.x

Optional (if uploading images):
- Pillow

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install django
```

Optional for image uploads:

```bash
python -m pip install pillow
```

## Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create admin user

```bash
python manage.py createsuperuser
```

## Run server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the home page and http://127.0.0.1:8000/admin/ for admin.

## Database

Default database is SQLite (`db.sqlite3`).

To use PostgreSQL or MySQL, update `DATABASES` in `workshop_management/settings.py`.

## Apps

- accounts: user profile extension
- assets: asset catalog and maintenance logs
- bookings: asset bookings
- inventory: materials and stock transactions
- dashboard: landing page and dashboard navigation

## Roles and permissions

Use Django's built-in `Group` and `Permission` models for role-based access control.
