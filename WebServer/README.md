# Web Server API
### Run Docker file

BUILD IMAGE: `$ docker build --tag flask-docker .`

RUN CONTAINER (FIRST TIME): `$ docker run --rm -p 5000:5000 -v ${PWD}:/WebServer flask-docker`

RUN TEST: `docker run --rm -p 5000:5000 -v ${PWD}:/WebServer flask-docker python manage.py test`