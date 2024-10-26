FROM ubuntu:focal

RUN useradd sandbox -m --home-dir /sandbox --uid 1111
VOLUME ["/sandbox"]

RUN apt-get update --fix-missing
RUN apt-get -y install build-essential
RUN apt-get -y upgrade

COPY docker/antoj-sandbox /root
RUN g++ /root/run.cpp -lpthread -o /usr/local/bin/run

CMD ["/bin/bash"]
