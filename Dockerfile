FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
RUN mkdir /log
RUN touch /log/django.log
RUN apt-get update
RUN apt-get install -y openslide-tools
RUN apt-get install -y curl gnupg gnupg2 
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs 
RUN npm install -g yarn typescript
RUN cd slack-logger && npm install && yarn build
ENV http_proxy host:port
ENV https_proxy host:port