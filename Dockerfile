FROM ubuntu:latest

# netbase - deal with issue where python can't find the tcp network protocol
# build essential is needed for psycopg2
# must have python 3.8 installed
# libpq-dev for psycopg2
RUN apt-get update && \
    apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall netbase && \
    apt-get install -y --no-install-recommends \
    build-essential python3.8 python3-pip python3.8-dev libpq-dev

#server host port
EXPOSE 3091

WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3.8", "sockets.py" ]