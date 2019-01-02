FROM node:10.14.2
RUN npm install -g yarn
RUN mkdir -p /code_front
WORKDIR /code_front
ADD package.json /code_front/
RUN npm install
ADD . /code_front/
ENV http_proxy host:port
ENV https_proxy host:port