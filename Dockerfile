FROM python:3.8-slim-buster

WORKDIR /app
COPY . /app/
RUN python -m venv venv
RUN . venv/bin/activate

RUN pip install -r requirements.txt
RUN python ./setup.py test

ENV LISTEN_PORT=80
EXPOSE 80
WORKDIR /app/api
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]