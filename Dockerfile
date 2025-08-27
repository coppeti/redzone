FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# On enlève collectstatic d'ici !

EXPOSE 8000

# On fait collectstatic au démarrage à la place
CMD python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 config.wsgi:application