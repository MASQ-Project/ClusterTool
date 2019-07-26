# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
FROM ubuntu:devel

RUN apt-get update && \
    apt-get install -y curl wget procps sqlite3

ENV SUDO_UID 1000
ENV SUDO_GID 1000

COPY metrics.sh ./
