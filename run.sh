#!bin/bash
pipenv run python manage.py runserver 0.0.0.0:8000
pipenv run celery -A campaign_system worker -l info
pipenv run celery -A campaign_system beat -l info
