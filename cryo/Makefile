IMAGE ?= cryo:latest
CRYO_REF ?= main
UID ?= $(shell id -u)
GID ?= $(shell id -g)
PWD := $(shell pwd)

.PHONY: install cli

install:
	docker build --build-arg CRYO_REF=$(CRYO_REF) -t $(IMAGE) .

cli: install
	docker run --rm -it \
		--user $(UID):$(GID) \
		-v /etc/passwd:/etc/passwd:ro \
		-v /etc/group:/etc/group:ro \
		-e HOME=/work \
		-e USER=$(shell id -un) \
		--entrypoint bash \
		-v $(PWD):/work \
		-w /work \
		$(IMAGE)
