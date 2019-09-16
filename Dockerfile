# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
FROM debian:buster-slim

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y procps
RUN apt-get install -y sqlite3

ENV SUDO_UID 1000
ENV SUDO_GID 1000

COPY metrics.sh ./
