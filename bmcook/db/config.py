from os import environ

db_name = environ.get("PG_DB_NAME", "moon")
db_user = environ.get("PG_DB_USER", "moon")
db_password = environ.get("PG_DB_PASS", "moon")
db_host = environ.get("PG_DB_HOST", "localhost")
db_port = environ.get("PG_DB_PORT", 5432)
