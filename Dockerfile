FROM python:3.8-slim-buster

WORKDIR /app
COPY . /app/
RUN python -m venv venv
RUN . venv/bin/activate

ENV FLASK_APP=api

RUN pip install -r requirements.txt
RUN python ./setup.py test

EXPOSE 80
WORKDIR /app/api
ENTRYPOINT ["flask", "run"]