# Web Server API
### Run Docker file

BUILD IMAGE: `$ docker build --tag flask-docker .`

RUN CONTAINER (FIRST TIME): `$ docker run -p 5000:5000 -v ${PWD}:/WebServer flask-docker`

START CONTAINER: ``$ docker start -a -i `docker ps -q -l` ``