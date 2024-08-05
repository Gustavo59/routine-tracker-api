api-up:
	@echo "Running api on port 8005"
	@uvicorn src.routine_tracker_core.external_interfaces.routine_tracker_api.main:app --reload --host 0.0.0.0 --port 8005

clean:
	@echo "Running black and isort"
	@black . && isort .

lint:
	@echo "Running flake8"
	@flake8

docker:
	@echo "Buildando e subindo docker"
	@docker compose up --build -d

before-commit: clean lint