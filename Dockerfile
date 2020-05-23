FROM ubuntu:18.04
RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python python-pip python-dev
WORKDIR /app
COPY . /app/
RUN python -m pip install -r requirements.txt
WORKDIR /app/api
CMD ["python", "api,py"]