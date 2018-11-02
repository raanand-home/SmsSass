
build-test:
	docker-compose -f \
		tests/docker-compose.yml build
up: build-test
	docker-compose -f tests/docker-compose.yml up -d
down:
	docker-compose -f tests/docker-compose.yml down
test: build-test up
	docker-compose -f tests/docker-compose.yml up -d
	make pytest ; (ret=$$?; make down || exit $$ret)
pytest: venv
	./venv/bin/py.test
venv:
	virtualenv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install -r web-app/requirements.txt
pep8: venv
	./venv/bin/pep8 web-app/
	./venv/bin/pep8 mock-sms-service/
swagger.json:
	@make up
	curl http://localhost:5000/swagger.json
	@make down
clean:
	rm -rf venv
