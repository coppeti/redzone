FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Ajoute user non root (optionnel mais recommandé)
RUN adduser --disabled-password myuser
USER myuser

# Collecte les fichiers statiques
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000