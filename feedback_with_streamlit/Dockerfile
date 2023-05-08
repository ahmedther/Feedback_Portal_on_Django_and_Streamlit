FROM python:3.11.3-slim

LABEL maintainer='ahmed'

ENV PYTHONUNBUFFERED 1

WORKDIR /feedback_and_streamlit

COPY ./ ./

RUN apt update -y --no-install-recommends \
    && apt upgrade -y --no-install-recommends \
    && apt install libpq-dev gcc curl unzip libaio1 -y \ 
    && python3 -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install --no-cache --no-cache-dir -r ./requirements.txt  \
    && chmod -R 777 /feedback_and_streamlit/ \
    && mkdir /var/log/uwsgi \
    && touch /var/log/uwsgi/feedback_and_streamlit.log  \ 
    && mkdir -p /cx_oracle \
    && cd /cx_oracle \
    && curl -o instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip https://download.oracle.com/otn_software/linux/instantclient/219000/instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && unzip -d . instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && rm -f instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
    && echo /cx_oracle/instantclient_21_9 > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig \
    && apt-get purge -y \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt autoremove -y  

ENV PATH="/py/bin:$PATH"

ENV LD_LIBRARY_PATH=/cx_oracle/instantclient_21_9

ENV PATH="/feedback_and_streamlit/scripts:/py/bin:$PATH"

EXPOSE 8005 8006


CMD ["./scripts/py_run.sh"]



# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     if [ $DEV = "true" ]; \
#     then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#     fi && \
#     rm -rf /tmp && \
#     adduser \
#     --disabled-password \
#     --no-create-home \
#     ahmed

