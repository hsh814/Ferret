FROM ubuntu:20.04
MAINTAINER Seungheon Han <hsh814@naver.com>

RUN mkdir /djbdns

COPY Djbdns/djbdns-1.05.tar.gz /djbdns/djbdns-1.05.tar.gz

ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  git \
  unzip \
  zlib1g-dev \
  wget \
  build-essential \
  gcc \
  g++ \
  libc6 \
  gzip \
  daemontools

WORKDIR /djbdns

RUN tar -xzvf djbdns-1.05.tar.gz

WORKDIR /djbdns/djbdns-1.05

# RUN useradd -s /bin/false tinydns && \
#   useradd -s /bin/false dnslog && \
#   useradd -s /bin/false axfrdns

RUN echo gcc -O2 -include /usr/include/errno.h > conf-cc && \
  make && \
  make setup check && \
  tinydns-conf root root /etc/tinydns 0.0.0.0

WORKDIR /etc/tinydns/root
# Run eternal loop
CMD ["/bin/bash", "-c", "while :; do sleep 10; done"]