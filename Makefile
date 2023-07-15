serve:
	python3 app.py

deploy-local: create
	jprq http 5000 -s ebettengabackend

create:
	docker compose up -d
	docker exec -it crossed_server flask db upgrade

logs:
	docker compose logs -f
