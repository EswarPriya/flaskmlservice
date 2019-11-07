install:
	docker-compose run --rm server pip install -r requirements-dev.txt --user --upgrade --no-warn-script-location

start:
	docker-compose up server

prod-start:
	docker-compose up ProductonServe

coverage:
	docker-compose run --rm testserver bash -c "python -m pytest --cov-report term --cov-report html:coverage --cov-config setup.cfg --cov=src/ test/"

daemon:
	docker-compose up -d server

test:
	docker-compose run --rm testserver

lint:
	docker-compose run --rm server bash -c "python -m flake8 ./src ./test"

safety:
	docker-compose run --rm server bash -c "python vendor/bin/safety check"


build:
	docker build -t demo-api .

k-prod:
	docker kill demoApi-prod

r-prod:
	docker rm demoApi-prod

prod:
	docker run -d --name demoApi-prod --restart=unless-stopped --env-file='prod.env' -p 3008:3000 demo-api 

stagging:
	docker run --name demoApi-stagging --restart=unless-stopped --env-file='stagging.env' -p 3008:3000 demo-api  

k-stag:
	docker kill demoApi-stagging

r-stag:
	docker rm demoApi-stagging

