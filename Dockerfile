# abandoning this because I need to see 
# if I can access the host filesystem to query the directory that they provide

#


# FROM postgres:latest
FROM ubuntu:latest

# RUN python --version

# netbase - deal with issue where python can't find the tcp network protocol
# build essential is needed for psycopg2
# must have python 3.8 installed
# libpq-dev for psycopg2
RUN apt-get update && \
    apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall netbase && \
    apt-get install -y --no-install-recommends \
    build-essential python3.8 python3-pip python3.8-dev libpq-dev

# allow connection through this port
# EXPOSE 80

#server host port
EXPOSE 3091

# bundle the app
WORKDIR /usr/src/app
COPY . .

RUN pip3 install -r requirements.txt

# docker build -t steam-database-backend .
# docker run -p 80:80 -it steam-database-backend