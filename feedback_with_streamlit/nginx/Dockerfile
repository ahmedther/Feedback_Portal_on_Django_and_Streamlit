FROM nginx:alpine3.17-slim

LABEL maintainer='ahmed'

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./prx_run.sh ./prx_run.sh
COPY ./uwsgi_params /etc/nginx/uwsgi_params

CMD ["./prx_run.sh"]
