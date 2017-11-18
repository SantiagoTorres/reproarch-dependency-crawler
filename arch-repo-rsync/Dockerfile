FROM debian:stable-slim

LABEL maintainer="Santiago Torres-Arias <santiago@archlinux.org>"

RUN apt-get update && apt-get install --no-install-recommends rsync

COPY run-rsync.sh /run-rsync.sh

ENTRYPOINT run-rsync.sh
