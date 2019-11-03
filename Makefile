.PHONY: test clean

build:
	docker-compose -p DevOpsExercice build
run:
	docker-compose -p emailscraper up

