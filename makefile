install: 
	python3 -m venv venv
	pip install flask flask-pymongo

windows: 
	@echo "Windows Commands"
	venv\Scripts\activate
	flask -A __init__ --debug run

linux:
	@echo "Linux Commands"
	. venv/bin/activate
	flask -A __init__ --debug run