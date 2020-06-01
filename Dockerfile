FROM ubuntu:18.04
RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python3 python-pip python3-venv python-dev

WORKDIR /app
COPY . /app/
RUN python3 -m venv venv
RUN . venv/bin/activate
ENV FLASK_APP=api
RUN pip install -r requirements.txt

EXPOSE 8080
WORKDIR /app/api
ENTRYPOINT ["flask", "run", "-p", "8080"]