# Web Server API

### Run Docker file

BUILD IMAGE: `$ docker build --tag flask-docker .`

Per vedo:
RUN CONTAINER: `$ docker run --rm -p 5000:5000 -v ${PWD}:/WebServer flask-docker`

Per vinci:
RUN CONTAINER: `$ docker run --rm -p 5002:5000 -v ${PWD}:/WebServer flask-docker`

RUN TEST: `docker run --rm -p 5000:5000 -v ${PWD}:/WebServer flask-docker python manage.py test`

MIGTATE: 'docker run --rm -p 5002:5000 -v ${PWD}:/WebServer flask-docker python manage.py db init'
