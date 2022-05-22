run: avenv
	export FLASK_APP=articles.py
	avenv/bin/flask run
avenv: requirements.txt
	python3 -m venv avenv
	./avenv/bin/pip install -r requirements.txt
clean:
	rm -rf __pycache__
	rm -rf avenv