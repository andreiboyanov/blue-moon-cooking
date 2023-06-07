from os import environ

db_name = environ.get("POSTGRES_DATABASE", "moon")
db_user = environ.get("POSTGRES_USER", "moon")
db_password = environ.get("POSTGRES_PASSWORD", "moon")
db_host = environ.get("POSTGRES_HOST", "localhost")
db_port = environ.get("POSTGRES_PORT", 5432)
