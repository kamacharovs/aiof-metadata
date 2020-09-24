FROM python:3.8-slim-buster

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt
RUN python setup.py develop

ENV LISTEN_PORT=80
EXPOSE 80
WORKDIR /app/api
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]