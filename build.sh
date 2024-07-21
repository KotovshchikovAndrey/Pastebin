#!/bin/bash

docker-compose --env-file .env.docker up -d

sleep 5

export SLUG_POSTGRES_DB
export API_POSTGRES_DB

docker exec -it slug_postgres psql -U postgres -c "CREATE DATABASE ${SLUG_POSTGRES_DB} WITH ENCODING 'utf-8';"

docker exec -it slug_postgres psql -U postgres -d ${SLUG_POSTGRES_DB} -c "CREATE TABLE slug (id INT PRIMARY KEY GENERATED ALWAYS 
AS IDENTITY, is_released BOOLEAN NOT NULL DEFAULT FALSE);"

docker exec -it api_postgres psql -U postgres -c "CREATE DATABASE ${API_POSTGRES_DB} WITH ENCODING 'utf-8';"

sleep 5

docker-compose --env-file .env.docker restart api_microservice slug_microservice
