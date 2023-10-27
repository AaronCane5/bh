run:
	@echo "=== ++++++++++++ ==="
	@echo "=== Running app ==="
	@echo "=== ++++++++++++ ==="

	docker-compose -f docker-compose.dev.yml up --remove-orphans --build

build:
	@echo "=== ++++++++++++ ==="
	@echo "=== Building app ==="
	@echo "=== ++++++++++++ ==="

	docker build -t redwoodtwins/health_care_support .

push:
	@echo "=== ++++++++++++ ==="
	@echo "=== Pushing image ==="
	@echo "=== ++++++++++++ ==="

	docker push redwoodtwins/health_care_support