#!/bin/sh
exec gunicorn -b :5000 --access-logfile - --timeout 800 --error-logfile - faceapp:app