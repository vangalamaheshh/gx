FROM mvangala/base-conda:latest

MAINTAINER Mahesh Vangala <vangalamaheshh@gmail.com>

RUN set -ex \
  && git clone https://github.com/vangalamaheshh/pyftpdlib.git \
  && cd pyftpdlib \
  && python setup.py install

RUN set -ex \
  && pip install tornado \
  && pip install google-cloud-storage=1.7.0

RUN set -ex \
  && git clone https://github.com/vangalamaheshh/gx.git

EXPOSE 21

ENV AUTH_API ""
ENV PUBLIC_IP ""
ENV FTP_BUCKET ""
CMD ["python", "/usr/local/bin/gx/ftp/server.py"]
