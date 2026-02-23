#!/usr/bin/env bash

## bash script to start the PgAdmin container
mkdir -p 01_DOCKER_POSTGRESQL/pipeline/pgadmin_data

echo "Starting PgAdmin container..."

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v $(pwd)01_DOCKER_POSTGRESQL/pipeline/pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4