run: nvenv
	./nvenv/bin/python3 news/news/spiders/bbc_spider.py
	./nvenv/bin/python3 main.py jmark nekasifra
	rm articles.json
nvenv: requirements.txt
	python3 -m venv nvenv
	./nvenv/bin/python3 -m pip install --upgrade pip
	./nvenv/bin/pip install -r requirements.txt
clean:
	rm -rf __pycache__
	rm -rf nvenv