
run:
	poetry run python src/main.py

migrations/run:
	poetry run alembic upgrade head

docker/up:
	docker compose -f docker-compose.dev.yaml up 

docker/build:
	docker compose -f docker-compose.dev.yaml up --build

docker/run-migrations:
	docker compose -f docker-compose.dev.yaml exec app alembic upgrade head
