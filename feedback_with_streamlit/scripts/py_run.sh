#!/bin/sh

set -e


python manage.py collectstatic --noinput \

while true; do
  # Check if PostgreSQL server is available
  /py/bin/python /feedback_and_streamlit/scripts/check_postgres.py

  if [ $? -eq 0 ]; then
    break  # Break the loop if connection successful
  fi

  sleep 1
done


uwsgi --ini /feedback_and_streamlit/uwsgi/django_uwsgi.ini & \

streamlit run --server.port $SERVE_STREAMLIT_ON  /feedback_and_streamlit/app.py

uwsgi --ini /feedback_and_streamlit/uwsgi/streamlit_uwsgi.ini &

# python manage.py runserver 0.0.0.0:$SERVE_STREAMLIT_ON 
