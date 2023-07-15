serve:
	python3 app.py

deploy-local:
	jprq http 5000 -s ebettengabackend
