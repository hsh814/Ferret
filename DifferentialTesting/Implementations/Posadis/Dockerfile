FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y \
    autoconf \
    automake \
    dnsutils \
    gcc \
    git \
    libcap-dev \
    libnghttp2-dev \
    libtool \
    libtool-bin \
    libuv1-dev \
    libssl-dev \
    make \
    openssl \
    pkgconf \
    vim \
    nano

COPY Posadis/poslib-1.0.6-modified.tar.gz /root
COPY Posadis/posadis-0.60.6-modified.tar.gz /root

WORKDIR /root

RUN tar -xvf poslib-1.0.6-modified.tar.gz
RUN tar -xvf posadis-0.60.6-modified.tar.gz

WORKDIR /root/poslib-1.0.6
RUN ./configure
RUN make
RUN make install

WORKDIR /root/posadis-0.60.6
RUN ./configure
RUN make
RUN make install
RUN cp posadisrc /etc
RUN mkdir /etc/posadis

WORKDIR /root
CMD ["/bin/bash", "-c", "while :; do sleep 10; done"] 