FROM ubuntu:18.04
RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python python-pip python-virtualenv python-dev 
WORKDIR /app
COPY . /app/

RUN mkdir -p /venv/
RUN virtualenv /venv/
ENV PATH=/venv/bin:$PATH
ENV FLASK_APP=api
RUN /venv/bin/pip install -r /app/requirements.txt

EXPOSE 5000
WORKDIR /app/api
ENTRYPOINT ["flask", "run"]