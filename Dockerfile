# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
FROM debian:stable-slim

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y procps

ENV SUDO_UID 1000
ENV SUDO_GID 1000
