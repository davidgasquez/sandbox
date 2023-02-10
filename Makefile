IMAGE_NAME = davidgasquez/sandbox
IMAGE_TAG = latest

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

clean-build:
	docker build --no-cache -t $(IMAGE_NAME):$(IMAGE_TAG) .

push:
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

dev:
	docker run -it --rm -v $(PWD):/workspaces $(IMAGE_NAME):$(IMAGE_TAG) /bin/bash
