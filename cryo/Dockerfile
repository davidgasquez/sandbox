# syntax=docker/dockerfile:1

FROM rust:1-slim-bookworm AS builder

ARG CRYO_REF=main

WORKDIR /opt/cryo

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    pkg-config \
    libssl-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN cargo install --git https://github.com/paradigmxyz/cryo --branch ${CRYO_REF} --locked

FROM debian:bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    bash \
    libssl3 \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/cargo/bin/cryo /usr/local/bin/cryo

ENTRYPOINT ["cryo"]
