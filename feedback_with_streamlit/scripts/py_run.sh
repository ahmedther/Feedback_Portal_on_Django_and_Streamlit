#!/bin/sh

set -e

python manage.py collectstatic --noinput \

uwsgi --ini /feedback_and_streamlit/uwsgi/django_uwsgi.ini 

# uwsgi --ini /feedback_and_streamlit/uwsgi/streamlit_uwsgi.ini &