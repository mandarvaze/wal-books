#!/bin/bash
set -e

until psql "postgresql://$POSTGRES_USER@:5432" -c '\q'; do
  >&2 echo "Postgres is unavailable - waiting..."
  sleep 1
done

psql -v ON_ERROR_STOP=1 "postgresql://$POSTGRES_USER@:5432" <<-EOSQL
  DROP DATABASE IF EXISTS books_test;
  DROP USER IF EXISTS books_test;
  CREATE USER books_test WITH PASSWORD '';
  CREATE DATABASE books_test;
  GRANT ALL PRIVILEGES ON DATABASE books_test TO books_test;
EOSQL
