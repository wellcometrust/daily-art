FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

ENV WEB_CONCURRENCY=1

ENV APP_MODULE="daily-art.main:app"
ENV PORT=8000

RUN apt-get update && apt-get -y install cron
