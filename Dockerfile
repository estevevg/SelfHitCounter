FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3-dev python3-venv make

WORKDIR /opt/app

COPY . .