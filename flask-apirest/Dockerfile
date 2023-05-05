FROM ubuntu:20.04
RUN apt update
RUN apt install python3-dev python3-pip -y

WORKDIR /app-flask

COPY . /app-flask

RUN pip3 --no-cache-dir install -r requirements.txt
