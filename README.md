# django-imageboard

Image gallery site based on the Django Framework

virtualenv venv -p python3
source venv/bin/activate
pip install requirements
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Set a secret key for the development

Generate a secret key using the following command:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Set the generated secret key as an environment variable:
export SECRET_KEY='NEW_KEY_GENERATED_IN_STEP1'

P.S
DEBUG is enabled by default. To disable it, set the environment variable.
