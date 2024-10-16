FROM python:3.10.12-alpine3.18

#FROM python:3.10.12-slim-bullseye

# FROM python:3.13.0-slim
# FROM python:3.10.13-bookworm
#FROM arm32v7/alpine:3.18.4

WORKDIR /app

COPY ./requirements.txt .
RUN apk update && pip install -r requirements.txt

COPY ./main.py .
COPY ./src/ ./src/
COPY ./res/ ./res/


#RUN apt-get update \
#	&& apt-get -y install enchant-2 \
#	&& pip install -r requirements.txt

EXPOSE 5000
CMD waitress-serve --host 0.0.0.0 --port 5000 --call src.app:create_app
#CMD tail -f /dev/null
