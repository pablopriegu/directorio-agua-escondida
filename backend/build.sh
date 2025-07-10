#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py create_initial_data # <-- AÑADE ESTA LÍNEA