IMAGE_NAME = "rocm:mine"

build:
	docker build --no-cache -t $(IMAGE_NAME) .

dev:
	docker run -it --network=host --device=/dev/kfd \
		--device=/dev/dri --group-add=video --ipc=host \
		--cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
		-v $(PWD):/home/rocmer \
		$(IMAGE_NAME) /bin/bash
