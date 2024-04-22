IMAGE_NAME := filecoin/lily:master-202404181000-a2a6dccb-calibnet
SNAPSHOT_URL := https://forest-archive.chainsafe.dev/calibnet/latest/forest_snapshot_calibnet_2024-04-22_height_1548131.forest.car.zst

dev:
	docker run -it \
		--entrypoint /bin/bash \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE_NAME)

snapshot:
	wget -O snapshot.forest.car.zst $(SNAPSHOT_URL)
