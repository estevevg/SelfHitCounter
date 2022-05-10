build:
	docker build -t hit-counter -f Dockerfile.web .

start:
	docker run --rm -dit --name my-apache-app -p 8080:80 -v $(shell pwd)/src:/usr/local/apache2/htdocs/ httpd:2.4

stop:
	docker stop my-apache-app

env_ok: requirements.txt
	rm -rf env env_ok
	python3 -m venv env
	env/bin/pip install -U pip
	env/bin/pip install -r requirements.txt
	touch env_ok

.PHONY: fmt
fmt: env_ok
	env/bin/isort -sp .isort.cfg $(py_files)
	env/bin/black $(py_files)

.PHONY: test
test: env_ok
	env/bin/python -m unittest discover $(py_dirs) -p "*.py" -v
