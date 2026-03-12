# JVR: Snippets
```bash
# build container:version from 00_DENG_HW/ root
docker build -f 01_DOCKER_POSTGRESQL/pipeline/Dockerfile -t test:pandas .

docker build -f 01_DOCKER_POSTGRESQL/pipeline/Dockerfile -t taxi_ingest:v001 .
```

```bash
# mount volume
docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \
    --entrypoint=bash \
    python:3.13.11-slim
```

```bash
# name container
docker run -it \
    --name my-deng \
    --entrypoint=bash \
    python:3.13.11-slim

docker start -ai my-deng
```

```bash
# run with arguments
docker run -it test:pandas 42
```

```bash
# convert the notebook to a Python script:
uv run jupyter nbconvert --to=script 01_DOCKER_POSTGRESQL/pipeline/notebook.ipynb 
mv 01_DOCKER_POSTGRESQL/pipeline/notebook.py 01_DOCKER_POSTGRESQL/pipeline/ingest_data.py
```

The script reads data in chunks (100,000 rows at a time) to handle large files efficiently without running out of memory.


Make sure PostgreSQL is running, then execute the ingestion script:

```bash
uv run python 01_DOCKER_POSTGRESQL/pipeline/ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips \
  --year=2021 \
  --month=1 \
  --chunksize=100000
```

Check postgres ingestion results
```sql
-- Count records (should return 1,369,765 rows)
SELECT COUNT(*) FROM yellow_taxi_trips;

-- View sample data
SELECT * FROM yellow_taxi_trips LIMIT 10;

-- Basic analytics
SELECT 
    DATE(tpep_pickup_datetime) AS pickup_date,
    COUNT(*) AS trips_count,
    AVG(total_amount) AS avg_amount
FROM yellow_taxi_trips
GROUP BY DATE(tpep_pickup_datetime)
ORDER BY pickup_date;
```


**Run pgAdmin Container**

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4
```

**Docker Networks**

Let's create a virtual Docker network called `pg-network`:

```bash
docker network create pg-network
```

> You can remove the network later with the command `docker network rm pg-network`. You can look at the existing networks with `docker network ls`.

Stop both containers and re-run them with the network configuration:

```bash
# Run PostgreSQL on the network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

# In another terminal, run pgAdmin on the same network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```


```bash
docker-compose up
```

```bash
docker-compose down
```

And if you want to run the containers again in the background rather than in the foreground (thus freeing up your terminal), you can run them in detached mode:

```bash
docker-compose up -d
```

Other useful commands:

```bash
# View logs
docker-compose logs

# Stop and remove volumes
docker-compose down -v
```

# Cleanup

When you're done with the workshop, clean up Docker resources to free up disk space:

**Stop all running containers:**
```bash
docker-compose down
```

**Remove specific containers:**
```bash
# List all containers
docker ps -a

# Remove specific container
docker rm <container_id>

# Remove all stopped containers
docker container prune
```

**Remove Docker images:**
```bash
# List all images
docker images

# Remove specific image
docker rmi taxi_ingest:v001
docker rmi test:pandas

# Remove all unused images
docker image prune -a
```

**Remove Docker volumes:**
```bash
# List volumes
docker volume ls

# Remove specific volumes
docker volume rm ny_taxi_postgres_data
docker volume rm pgadmin_data

# Remove all unused volumes
docker volume prune
```

**Remove Docker networks:**
```bash
# List networks
docker network ls

# Remove specific network
docker network rm pg-network

# Remove all unused networks
docker network prune
```

**Complete cleanup (removes everything):**
```bash
# ⚠️ Warning: This removes ALL Docker resources!
docker system prune -a --volumes
```

**Clean up local files:**
```bash
# Remove parquet files
rm *.parquet

# Remove Python cache
rm -rf __pycache__ .pytest_cache

# Remove virtual environment (if using venv)
rm -rf .venv
```


## Terraform
```tf

```