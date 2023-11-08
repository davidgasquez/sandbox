FROM ubuntu

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Iroh
RUN curl -fsSL https://sh.iroh.computer/install.sh | sh

WORKDIR /iroh
