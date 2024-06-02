up:
	sudo docker compose -f docker-compose-FastDate.yaml up -d 

down:
	sudo docker compose -f docker-compose-FastDate.yaml down && network prune --force
