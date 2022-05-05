build:
	docker build -t hit-counter .

start:
	docker run --rm -dit --name my-apache-app -p 8080:80 -v $(shell pwd)/app/src/:/usr/local/apache2/htdocs/ httpd:2.4
