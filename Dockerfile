FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq \
        cron

ENV WEB_CONCURRENCY=1

ENV APP_MODULE="daily-art.main:app"
ENV PORT=8000

COPY . /app
