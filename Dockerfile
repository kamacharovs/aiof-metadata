FROM ubuntu:18.04
RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python3 python3-pip python3-venv python-dev
WORKDIR /app
COPY . /app/

RUN python3 -m venv venv
RUN . venv/bin/activate
ENV FLASK_APP=api
RUN /venv/bin/pip3 install -r /app/requirements.txt

EXPOSE 5000
WORKDIR /app/api
ENTRYPOINT ["flask", "run"]