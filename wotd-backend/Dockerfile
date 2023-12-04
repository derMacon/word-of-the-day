# FROM python:3.10.13-bookworm
# FROM python:3.9.18-slim-bullseye

FROM arm32v7/alpine:3.18.4

WORKDIR /app


COPY ./main.py .
COPY ./requirements.txt .
COPY ./src/ ./src/
COPY ./res/ ./res/

RUN apk update \
	&& apk add --no-cache python3 py3-pip \
	&& pip install -r requirements.txt

EXPOSE 5000
CMD python3 main.py
