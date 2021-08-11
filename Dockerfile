FROM python:3.8-alpine
MAINTAINER Fredrick Njeri.
ENV PYTHONUNBUFFERED 1
RUN mkdir /volaa
WORKDIR /volaa
COPY . /volaa
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev \
      && apk add postgresql jpeg-dev zlib-dev libjpeg \
      && pip3 install psycopg2 Pillow
RUN pip3 install -r /volaa/requirements.txt
RUN apk del .tmp-build-deps
RUN adduser -D volaa
USER volaa
