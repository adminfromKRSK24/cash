#!/bin/sh
set -e

# Применяем миграции
python3 ./manage.py makemigrations --noinput
python3 ./manage.py migrate --noinput

# Создаем суперпользователя dev/123, если его нет
python3 ./manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_NAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username="dev").exists():
    User.objects.create_superuser(username=username, email=email, password=password)

# --- Статусы ---
statuses = ["Бизнес", "Личное", "Налог"]
for s in statuses:
    Status.objects.get_or_create(name=s)

# --- Типы ---
types = ["Пополнение", "Списание"]
for t in types:
    Type.objects.get_or_create(name=t)

# --- Категории и подкатегории ---
type_pop, _ = Type.objects.get_or_create(name="Пополнение")
type_exp, _ = Type.objects.get_or_create(name="Списание")

cat_infra, _ = Category.objects.get_or_create(name="Инфраструктура", type=type_exp)
SubCategory.objects.get_or_create(name="VPS", category=cat_infra)
SubCategory.objects.get_or_create(name="Proxy", category=cat_infra)

cat_marketing, _ = Category.objects.get_or_create(name="Маркетинг", type=type_exp)
SubCategory.objects.get_or_create(name="Farpost", category=cat_marketing)
SubCategory.objects.get_or_create(name="Avito", category=cat_marketing)

# --- Тестовые записи в History ---
if History.objects.count() == 0:
    h1 = History.objects.create(
        date=timezone.now(),
        status=Status.objects.get(name="Бизнес"),
        type=type_exp,
        category=cat_infra,
        subcategory=SubCategory.objects.get(name="VPS", category=cat_infra),
        amount=Decimal("5000.00"),
        comment="Оплата VPS сервера"
    )

    h2 = History.objects.create(
        date=timezone.now(),
        status=Status.objects.get(name="Личное"),
        type=type_exp,
        category=cat_marketing,
        subcategory=SubCategory.objects.get(name="Avito", category=cat_marketing),
        amount=Decimal("2000.00"),
        comment="Реклама на Avito"
    )

    h3 = History.objects.create(
        date=timezone.now(),
        status=Status.objects.get(name="Налог"),
        type=type_exp,
        category=cat_infra,
        subcategory=SubCategory.objects.get(name="Proxy", category=cat_infra),
        amount=Decimal("1000.00"),
        comment="Оплата Proxy"
    )
    print("✅ Тестовые записи History созданы")
else:
    print("ℹ️  В таблице History уже есть данные")
EOF

# Запускаем команду, переданную в CMD
exec "$@"
