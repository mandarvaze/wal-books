.PHONY: all
all: .installed

.PHONY: install
install:
	@rm -f .installed  # force re-install
	@make .installed

.PHONY: dev
dev:
	@python manage.py runserver

.PHONY: unit
unit:
	@python manage.py test

.PHONY: format
format:
	@isort -rc books prj manage.py
	@black books prj manage.py

.PHONY: lint
lint:
	@flake8

.PHONY: tests
tests: unit format lint

# Start database in docker in foreground
.PHONY: pgsql
pgsql:
	@docker stop books-pgsql || true
	@docker rm books-pgsql || true
	@docker run -it --rm --name books-pgsql -v $(shell pwd)/.docker:/docker-entrypoint-initdb.d -p 5432:5432 postgres:12-alpine \
		postgres -c 'log_statement=all' -c 'max_connections=1000' -c 'log_connections=true'  -c 'log_disconnections=true'  -c 'log_duration=true'

# Start database in docker in background
.PHONY: start-pgsql
start-pgsql:
	docker start books-pgsql || docker run -d -v $(shell pwd)/.docker:/docker-entrypoint-initdb.d -p 5432:5432 --name books-pgsql postgres:12-alpine

.PHONY: clean-pgsql
clean-pgsql:
	@docker stop books-pgsql || true
	@docker rm books-pgsql || true

.PHONY: stop-pgsql
stop-pgsql:
	@docker stop books-pgsql || true
