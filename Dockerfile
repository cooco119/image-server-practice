FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
RUN mkdir /log
RUN touch /log/django.log
# RUN git clone https://github.com/cooco119/deepzoom.py.git
# RUN python3 deepzoom.py/setup.py install
ENV http_proxy host:port
ENV https_proxy host:port