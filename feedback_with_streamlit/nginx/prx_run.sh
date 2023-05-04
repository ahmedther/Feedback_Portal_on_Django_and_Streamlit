#!/bin/sh

set -e

apt-get autoremove -y
touch /etc/nginx/conf.d/default.conf
touch /var/log/nginx/feedback.log
touch /var/log/nginx/feedback_error.log
touch /var/log/nginx/streamlit.log
touch /var/log/nginx/streamlit_error.log
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'