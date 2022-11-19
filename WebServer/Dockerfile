# start by pulling the python image
FROM python:3.11-alpine
# copy the requirements file into the image
COPY requirements.txt requirements.txt
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

COPY . .

# This is the command that runs the application in the container
CMD flask --app mountainmates --debug run -h 0.0.0.0 -p 5000

# BUILD IMAGE >> docker build --tag flask-docker .
# RUN CONTAINER >> docker run -p 5000:5000 flask-docker