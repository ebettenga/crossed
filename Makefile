serve:
	python3 app.py

up:
	docker-compose up -d

deploy-local: create
	jprq http 5000 -s ebettengabackend

create:
	docker-compose up -d
	docker-compose exec -it server flask db upgrade
	docker-compose exec -it server python3 seed.py

down:
	docker-compose down

logs:
	docker compose logs -f
