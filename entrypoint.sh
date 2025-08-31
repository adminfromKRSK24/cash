#!/bin/sh
set -e

# Применяем миграции
python3 ./manage.py makemigrations --noinput
python3 ./manage.py migrate --noinput

# Создаем суперпользователя dev/123, если его нет
python3 ./manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_NAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username="dev").exists():
    User.objects.create_superuser(username=username, email=email, password=password)
EOF

# Запускаем команду, переданную в CMD
exec "$@"
