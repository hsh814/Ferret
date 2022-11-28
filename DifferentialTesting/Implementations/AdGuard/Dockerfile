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

# Install node.js
COPY node-v18.12.1-linux-x64.tar.xz /root
WORKDIR /root
RUN tar -xf node-v18.12.1-linux-x64.tar.xz
RUN update-alternatives --install /usr/bin/node node /root/node-v18.12.1-linux-x64/bin/node 1 \
    --slave /usr/bin/npm npm /root/node-v18.12.1-linux-x64/bin/npm \
    --slave /usr/bin/npx npx /root/node-v18.12.1-linux-x64/bin/npx \
    --slave /usr/bin/corepack corepack /root/node-v18.12.1-linux-x64/bin/corepack

# Install AdGuard
COPY AdGuardHome_linux_amd64.tar.gz /root
WORKDIR /root
RUN tar -xvf AdGuardHome_linux_amd64.tar.gz
WORKDIR /root/AdGuardHome
RUN ./AdGuardHome -s install