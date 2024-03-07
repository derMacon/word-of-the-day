#FROM python:3.8
FROM selenium/standalone-chrome:122.0

USER root

WORKDIR /app
COPY ./test.py .

RUN mkdir __logger

# install google chrome
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable

# install chromedriver
#RUN apt-get install -yqq unzip
# RUN wget -P /tmp https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux64/chrome-linux64.zip
# RUN unzip /tmp/chrome-linux64.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
#ENV DISPLAY=:99

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium

# RUN pip install --upgrade pip

# RUN pip install -r requirements.txt
#RUN pip install selenium

#CMD ["python", "./test.py"]
CMD tail -f /dev/null