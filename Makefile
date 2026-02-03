APP_CONTAINER = "secunda-backend"

up:
	docker compose up

seed:
	docker exec -ti $(APP_CONTAINER) uv run python cli.py

down:
	docker compose down

rebuild:
	docker compose down --volumes --remove-orphans
	docker compose build
	docker compose up

help:
	@echo "make up       - поднять контейнер приложения"
	@echo "make seed     - загрузка данных в БД из контейнера"
	@echo "make down     - остановить контейнеры"
	@echo "make rebuild  - пересобрать и поднять контейнеры"
