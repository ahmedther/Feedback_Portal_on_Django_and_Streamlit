

upstream feedback_app {
        server feedback:9005;
       
    }

server {
    listen ${LISTEN_PORT1};

    client_max_body_size 100m;
    client_body_buffer_size 100m;
    
    access_log /var/log/nginx/feedback.log;
    error_log /var/log/nginx/feedback_error.log;

    client_body_timeout 86400s;
    client_header_timeout 86400s;
    keepalive_timeout 86400s;
    send_timeout 86400s;



    location /static {
        root /feedback_and_streamlit;
    }

    location / {
        proxy_read_timeout 86400s;
        proxy_connect_timeout 86400s;
        proxy_send_timeout 86400s; 
        uwsgi_pass feedback_app;
        include /etc/nginx/uwsgi_params;

        # Set uWSGI timeout to one day (86400 seconds)
        uwsgi_read_timeout 8640;

    }

    location = /favicon.ico { access_log off; log_not_found off; }

   
}


