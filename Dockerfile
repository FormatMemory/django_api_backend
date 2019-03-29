FROM python:3.7-alpine
MAINTAINER FormatMemory <davidthinkleding@gmail.com>

ENV PYTHONUNBUFFERED 1
ARG TIME_ZONE
ARG TIME_ZONE

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN apk update
RUN apk upgrade
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        git \
        gcc \
        libc-dev \
        libffi-dev \
        linux-headers \
        build-base \
        py-mysqldb \
        mariadb-dev \
        mariadb-client \
        musl-dev \
        zlib \
        zlib-dev
        
RUN apk add ca-certificates && update-ca-certificates
RUN apk add --update --no-cache tzdata jpeg-dev
# Change TimeZone
# ENV TZ=America/Los_Angeles
ENV TZ=${TIME_ZONE}

COPY ./mysql_data/docker-entrypoint-initdb.d /docker-entrypoint-initdb.d
COPY ./mysql_data/mysql /var/lib/mysql

RUN pip install --upgrade setuptools
RUN pip install -r requirements/production.txt
RUN rm -rf .cache/pip
RUN apk del .tmp-build-deps

RUN adduser -D user
RUN chown -R user:user /app/static/
RUN chown -R user:user /app/media/
RUN chmod -R 755 /app/static/
RUN chmod -R 755 /app/media/
USER user

EXPOSE 8000
#CMD ["python", "manage.py", "migrate"]
