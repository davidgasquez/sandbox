test:
	docker run --rm ghcr.io/paradigmxyz/reth --version

dev:
	docker run --rm -it \
		-v $(PWD):/reth -w /reth \
		-p 9001:9001 \
		-p 30303:30303 \
		-p 30303:30303/udp \
		--entrypoint /bin/bash ghcr.io/paradigmxyz/reth
