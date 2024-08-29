#!/bin/ash

if [ "$FLASK_DEBUG" = '0' ]; then
  gunicorn --bind 0.0.0.0:5000 wsgi:app
else
  flask run --host=0.0.0.0 --port=5000
fi