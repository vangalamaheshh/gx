FROM mvangala/base-conda:latest

MAINTAINER Mahesh Vangala <vangalamaheshh@gmail.com>

RUN set -ex \
  && git clone https://github.com/vangalamaheshh/pyftpdlib.git \
  && cd pyftpdlib \
  && python setup.py install

RUN set -ex \
  && pip install tornado

RUN echo "Force"
RUN set -ex \
  && git clone https://github.com/vangalamaheshh/gx.git

EXPOSE 21
EXPOSE 60000-60100

ENV AUTH_API ""
CMD ["python", "/usr/local/bin/gx/ftp/server.py"]
