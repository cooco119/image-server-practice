# FROM node:10.14.2
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y curl gnupg gnupg2 
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs 
RUN npm install -g yarn
RUN mkdir -p /code_front
WORKDIR /code_front
ADD package.json /code_front/
RUN npm install
ADD . /code_front/
RUN echo "deb http://ppa.launchpad.net/nginx/stable/ubuntu bionic main" >> /etc/apt/sources.list
RUN apt-key add nginx_signing.key
RUN apt-get update
RUN mkdir -p /etc/nginx
RUN apt-get install -y nginx
RUN cp -f nginx.conf /etc/nginx/
RUN cp -f uwsgi_params /etc/nginx/
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	  && ln -sf /dev/stderr /var/log/nginx/error.log
CMD ["nginx", "-g", "daemon off;"]
RUN rm -rf /usr/share/nginx/html
RUN mkdir -p /usr/share/nginx/html/
RUN yarn build