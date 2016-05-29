#!/bin/bash
cd ..
HOST="127.0.0.1"
PORT="8888"
nohup python manage.py runserver $HOST:$PORT> /dev/null 2>&1 &

