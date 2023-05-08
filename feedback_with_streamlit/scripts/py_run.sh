#!/bin/sh

set -e

python manage.py collectstatic --noinput \

uwsgi --ini /feedback_and_streamlit/uwsgi/django_uwsgi.ini & \

streamlit run --server.port 8006  /feedback_and_streamlit/app.py

# uwsgi --ini /feedback_and_streamlit/uwsgi/streamlit_uwsgi.ini &