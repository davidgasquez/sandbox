cli:
	docker run --init -it --rm \
	--entrypoint /bin/bash \
	-v $(PWD)/data:/home/forest/data \
	--name forest \
	--network host \
	ghcr.io/chainsafe/forest:edge
