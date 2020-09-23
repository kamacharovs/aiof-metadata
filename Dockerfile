FROM ubuntu:18.04
RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get update

WORKDIR /app
COPY . /app/
RUN python3 -m venv venv
RUN . venv/bin/activate
ENV FLASK_APP=api
RUN pip3 install -r requirements.txt
RUN python3 ./setup.py test

EXPOSE 8080
WORKDIR /app/api
ENTRYPOINT ["flask", "run", "-p", "8080"]