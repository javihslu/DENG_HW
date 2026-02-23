#!/usr/bin/env bash

## bash script to run the ingestion container
echo "Running data ingestion for January 2021..."

# check the network link:
docker network ls 

# it's pipeline_default
# now run the script:
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips_2021_2 \
    --year=2021 \
    --month=2 \
    --chunksize=100000