FROM mcr.microsoft.com/devcontainers/universal:linux

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends make
