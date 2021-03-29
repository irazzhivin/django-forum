# django-imageboard

Image gallery site based on the Django Framework

## Getting Started

Run following commands to start project in your enviroment:

```
virtualenv venv -p python3
source venv/bin/activate

pip install requirements

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Feutures

1. User can create gallery and upload multiple images in one.
2. User can update and delete single gallery images.
3. Admin managment

TODO: create comments block under gallery

## To use in prod:
1. Set a secret key for the development

Generate a secret key using the following command:
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Set the generated secret key as an environment variable:
```
export SECRET_KEY='NEW_KEY_GENERATED_IN_STEP1'
```

2. DEBUG is enabled by default. To disable it, set the environment variable.
