up:
	sudo docker compose -f docker-compose-helperrss.yaml up -d && docker-compose exec helper_rss_bot bash

down:
	sudo docker compose -f docker-compose-helperrss.yaml down && network prune --force
