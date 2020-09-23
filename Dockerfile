FROM python:3.8-slim-buster

WORKDIR /app
COPY . /app/
RUN python3 -m venv venv
RUN . venv/bin/activate

ENV FLASK_APP=api

RUN pip3 install -r requirements.txt
RUN python3 ./setup.py test

EXPOSE 80
WORKDIR /app/api
ENTRYPOINT ["flask", "run"]