serve:
	python app.py

deploy-local:
	jprq http 5000 -s ebettengabackend
