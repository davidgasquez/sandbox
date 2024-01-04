IMAGE_NAME = "iroh"

build:
	docker build -t $(IMAGE_NAME) .

dev: build
	docker run -it --rm -v $(PWD):/iroh $(IMAGE_NAME) /bin/bash

node:
	export IROH_DATA_DIR=./iroh && iroh start --rpc-port 3000
