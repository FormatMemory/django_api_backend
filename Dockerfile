FROM python:3.7-alpine
MAINTAINER FormatMemory <davidthinkleding@gmail.com>

ENV PYTHONUNBUFFERED 1
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

RUN mkdir -p /media
RUN mkdir -p /static
RUN chown -R user:user /static/
RUN chown -R user:user /media/
RUN chmod -R 755 /static/
RUN chmod -R 755 /media/
USER user

EXPOSE 8000
#CMD ["python", "manage.py", "migrate"]
# CMD ["gunicorn", "-c", "gunicorn_conf.py", "--chdir", "app", "app.wsgi:application", "--reload"]
# RUN python manage.py wait_for_db
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput
# CMD ["gunicorn", "-c", "gunicorn_conf.py", "app.wsgi:application", "--reload"]
