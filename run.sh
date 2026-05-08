#!/bin/sh
gunicorn backend.wsgi --log-file -
