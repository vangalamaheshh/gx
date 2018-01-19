FROM mvangala/base-conda:latest

MAINTAINER Mahesh Vangala <vangalamaheshh@gmail.com>

RUN set -ex \
  && git clone https://github.com/vangalamaheshh/pyftpdlib.git \
  && cd pyftpdlib \
  && python setup.py install

RUN set -ex \
  && git clone https://github.com/vangalamaheshh/gx.git

EXPOSE 21

CMD ["python", "/usr/local/bin/gx/ftp/server.py"]
