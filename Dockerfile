FROM ubuntu:18.04
RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python python-pip python-dev
WORKDIR /app
COPY . /app/
RUN pip install .
WORKDIR /app/api
ENTRYPOINT ["python"]
CMD ["api.py"]