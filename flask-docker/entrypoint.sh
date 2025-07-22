#!/bin/sh

# Flask 애플리케이션을 Gunicorn으로 실행
gunicorn --workers 2 --bind 0.0.0.0:8000 main:app

