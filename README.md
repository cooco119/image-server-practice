# image-server-practice

#### requiremenst.txt : dependant modules needed to be installed after starting venv
`source .env/bin/activate && pip3 install -r requirements.txt`

> virtualenv path could differ by environments

# Docker Setup

~#### Setup & Connect to docker machine ~

~from https://docs.docker.com/machine/get-started/~
```
~docker-machine create --driver virtualbox default~
~docker-machine env~
~eval $(docker-machine env)~
```

~Setup port forwarding rule for VM -> docker engine(inside VM)~

~`VBoxManage modifyvm default --natpf1 "pf1,tcp,,8000,,8000"`~

~Start docker machine~
~`docker-machine start default`~

#### Build docker-compose
```
docker-compose down
docker-compose build 
docker-compose run web python3 manage.py migrate
docker-compose up
```

#### Accessing django server

First, find local ip address for VirtualBox machine(Docker Machine)

`docker-machine ls`

or

`docker-machine ip default`

In local environment, access the server through the ip address & port
ex)

`http://192.168.99.100:3000'

-> this is available in LAN environment too.

