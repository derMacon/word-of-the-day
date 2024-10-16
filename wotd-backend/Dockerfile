#FROM python:3.10.12-alpine3.18
FROM python:3.10.12-slim-bullseye

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update \
	&& apt-get -y install enchant-2 \
    && apt-get -y install hunspell-de-de \
    && apt-get -y install hunspell-fr \
	&& pip install -r requirements.txt

COPY ./main.py .
COPY ./src/ ./src/
COPY ./res/ ./res/

EXPOSE 5000
CMD python main.py
#CMD tail -f /dev/null
