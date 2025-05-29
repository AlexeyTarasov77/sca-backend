
run:
	poetry run python src/main.py

migrations/run:
	poetry run alembic upgrade head
