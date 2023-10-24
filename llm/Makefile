IMAGE_NAME = "rocm:mine"

build:
	docker build --no-cache -t $(IMAGE_NAME) .

model:
	wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf

dev:
	docker run -it --network=host --device=/dev/kfd \
		--device=/dev/dri --group-add=video --ipc=host \
		--cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
		--entrypoint=bash \
		-v $(PWD):/models \
		$(IMAGE_NAME)
