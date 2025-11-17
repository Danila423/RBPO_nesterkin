IMAGE_NAME=course-app:local

.PHONY: build up down lint-docker scan trivy

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down -v

lint-docker:
	hadolint Dockerfile

scan:
	trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed $(IMAGE_NAME)
