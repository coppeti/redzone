FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /redzone

WORKDIR /redzone

COPY requirements.txt /redzone/
RUN pip install -r requirements.txt

COPY . /redzone

RUN python manage.py collectstatic --noinput

RUN chmod +x /redzone/entrypoint.sh