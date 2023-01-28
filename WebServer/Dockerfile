# start by pulling the python image
FROM python:3.11-alpine
# copy the requirements file into the image
COPY requirements.txt requirements.txt
# install the dependencies and packages in the requirements file
RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index numpy
RUN pip install -r requirements.txt

VOLUME /WebServer

WORKDIR /WebServer

ENV FLASK_APP=app/__init__.py

# This is the command that runs the application in the container
#CMD flask --app mountainmates --debug run -h 0.0.0.0 -p 5000
#CMD export FLASK_APP=app/main/__init__.py

CMD python manage.py run -h 0.0.0.0
