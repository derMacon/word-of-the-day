FROM python:3.10.12-slim-bullseye
# FROM python:3.13.0-slim
# FROM python:3.10.13-bookworm
#FROM arm32v7/alpine:3.18.4

WORKDIR /app


COPY ./main.py .
COPY ./requirements.txt .
COPY ./src/ ./src/
COPY ./res/ ./res/

#RUN apk update \
#	&& apk add --no-cache python3 py3-pip \
#	&& pip install -r requirements.txt

RUN apt-get update

# RUN apt-get update \
# 	&& pip install -r requirements.txt

EXPOSE 5000
# CMD python3 main.py
CMD tail -f /dev/null
