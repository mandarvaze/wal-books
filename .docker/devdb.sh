#!/bin/bash
set -e

until psql "postgresql://$POSTGRES_USER@:5432" -c '\q'; do
  >&2 echo "Postgres is unavailable - waiting..."
  sleep 1
done

psql -v ON_ERROR_STOP=1 "postgresql://$POSTGRES_USER@:5432" <<-EOSQL
  DROP DATABASE IF EXISTS books_dev;
  DROP USER IF EXISTS books_dev;
  CREATE USER books_dev WITH PASSWORD '';
  CREATE DATABASE books_dev;
  GRANT ALL PRIVILEGES ON DATABASE books_dev TO books_dev;
EOSQL
