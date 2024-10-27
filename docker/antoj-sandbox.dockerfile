FROM ubuntu:focal

RUN useradd sandbox -m --home-dir /sandbox --uid 1111
VOLUME ["/sandbox"]

# OpenJDK installation needs user to select their time zone.
# Add `DEBIAN_FRONTEND=noninteractive` to enable non-interactive installation.
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update --fix-missing

# c, cpp
RUN apt-get install -y build-essential clang

# python2, python3
RUN apt-get install -y python2 python3

# java
RUN apt-get install -y openjdk-17-jdk-headless

# haskell
RUN apt-get install -y ghc

# rust
RUN apt-get install -y rustc

# go
RUN apt-get install -y golang

# ruby
RUN apt-get install -y ruby

# csharp
RUN apt-get install -y mono-mcs

# pascal
# # Wonder why it fails. Just skip it LOL.
# RUN apt-get install -y fpc

# nodejs
RUN apt-get install -y curl && \
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
  apt-get install -y nodejs

# swift
# # This also fails.
# RUN apt-get install -y software-properties-common && \
#   add-apt-repository ppa:swiftlang/ppa && \
#   apt-get update && apt-get install -y swift

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY docker/antoj-sandbox /root
RUN g++ /root/run.cpp -lpthread -o /usr/local/bin/run

CMD ["/bin/bash"]
