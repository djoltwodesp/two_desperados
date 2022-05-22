run: avenv
	avenv/bin/flask run
avenv: requirements.txt
	python3 -m venv avenv
	./avenv/bin/python3 -m pip install --upgrade pip
	./avenv/bin/pip install -r requirements.txt
clean:
	rm -rf __pycache__
	rm -rf avenv