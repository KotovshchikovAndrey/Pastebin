# Pastebin

# Запуск

1. docker-compose --env-file <.env файл> up -d
2. export SLUG_POSTGRES_DB=<название базы данных>
3. export API_POSTGRES_DB=<название базы данных>
4. docker exec -it slug_postgres psql -U postgres -c "CREATE DATABASE ${SLUG_POSTGRES_DB} WITH ENCODING 'utf-8';"
5. docker exec -it slug_postgres psql -U postgres -d ${SLUG_POSTGRES_DB} -c "CREATE TABLE slug (id INT PRIMARY KEY GENERATED ALWAYS 
AS IDENTITY, is_released BOOLEAN NOT NULL DEFAULT FALSE);"
6. docker exec -it api_postgres psql -U postgres -c "CREATE DATABASE ${API_POSTGRES_DB} WITH ENCODING 'utf-8';"
7. docker-compose --env-file .env.docker restart api_microservice slug_microservice
