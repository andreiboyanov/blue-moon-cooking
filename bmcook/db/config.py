from os import environ

db_name = environ.get("PG_DB", "moon")
db_user = environ.get("PG_USER", "moon")
db_password = environ.get("PG_PASS", "moon")
db_host = environ.get("PG_HOST", "localhost")
db_port = environ.get("PG_PORT", 5432)
