install: 
	pip install python-gnupg hashlib 
	python3 -m venv venv
	pip install flask flask_pymongo

windows: 
	@echo "Windows Commands"
	venv\Scripts\activate
	flask -A __init__ --debug run

linux:
	@echo "Linux Commands"
	. venv/bin/activate
	flask -A __init__ --debug run

list:
	@echo "Listing Secret Keys"
	gpg --list-secret-keys --keyid-format=long
	@echo "Listing all keys..."
	gpg --list-keys
deletescrkey:
	@read -p "Enter userid to delete: " uid; \
	gpg --delete-secret-key $$uid
deletekey:
	make deletescrkey
	@read -p "Enter userid to delete: " uid; \
	gpg --delete-key $$uid