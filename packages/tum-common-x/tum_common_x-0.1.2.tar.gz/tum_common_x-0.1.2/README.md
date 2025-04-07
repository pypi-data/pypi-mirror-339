# My Django Base

A reusable Django application that serves as a foundation for other projects.

## Installation

```bash
pip install my-django-base
```

## Usage

1. Add to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'my_django_base',
    ...
]
```

2. Include the URLs:

```python
urlpatterns = [
    ...
    path('base/', include('my_django_base.urls')),
    ...
]
```

3. Run migrations:

```bash
python manage.py migrate
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Customization

Describe how to extend or customize your base application.

## License

MIT License
