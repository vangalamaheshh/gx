FROM mvangala/base-nginx:python3.6

MAINTAINER Mahesh Vangala <vangalamaheshh@gmail.com>

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN set -ex \
  && pip install flask \
  && pip install py2neo 

WORKDIR /usr/local/bin

RUN set -ex \
  && git clone https://github.com/vangalamaheshh/gx.git

# set up flask with nginx
# By default, allow unlimited file sizes, modify it to limit the file sizes
# To have a maximum of 1 MB (Nginx's default) change the line to:
# ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_MAX_UPLOAD 0

# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /usr/local/bin/gx/graph-api/uwsgi.ini
# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /usr/local/bin/gx/graph-api/static
# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /usr/local/bin/gx/graph-api

CMD ["/usr/bin/supervisord"]
