cli:
	docker run --init -it --rm \
	--entrypoint /bin/bash \
	-v $(PWD)/snapshots:/home/forest/snapshots \
	--name forest \
	--network host \
	ghcr.io/chainsafe/forest:edge

clean-docker-image:
	docker rmi ghcr.io/chainsafe/forest:edge
