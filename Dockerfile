FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt
RUN python setup.py develop

WORKDIR /app/tests
RUN pytest

ENV APP_MODULE=api.api:app
ENV HOST=0.0.0.0
ENV LISTEN_PORT=80
ENV PORT=80