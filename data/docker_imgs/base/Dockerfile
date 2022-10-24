
FROM ubuntu:20.04

MAINTAINER fmtz 

RUN apt update 

RUN apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

ENV TZ="America/Sao_Paulo"

RUN apt install -y python3 python3-pip python3-venv python-is-python3 build-essential cmake vim tmux 

RUN python -m pip install numpy 
