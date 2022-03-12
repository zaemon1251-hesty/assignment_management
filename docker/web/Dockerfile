# base image
FROM nginx:latest

COPY ./docker/web/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/web/ssl /etc/nginx/ssl

ENTRYPOINT ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]