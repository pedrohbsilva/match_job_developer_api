run-app:
	docker-compose up --build

run-db:
	docker-compose -f docker-compose-db.yml up --build  

run-debug:
	docker-compose build && docker-compose run --service-ports app

run-stop:
	docker-compose down 

run-prune:
	docker-compose -f docker-compose-db.yml down && docker-compose down

createdb:
	docker-compose exec app python manage.py recreate_db

populatedb:
	docker-compose exec app python manage.py populate_db

heroku_create:
	heroku create

heroku_login: 
	heroku container:login 

heroku_postgres:
	heroku addons:create heroku-postgresql:hobby-dev --app lit-citadel-12163

heroku_registry:
	docker build -f Dockerfile.prod -t registry.heroku.com/lit-citadel-12163/web .

heroku_run-local:
	docker run --name flask -e "PORT=8765" -p 5005:8765 registry.heroku.com/lit-citadel-12163/web:latest

heroku_remove:
	docker rm flask

heroku_push:
	docker push registry.heroku.com/lit-citadel-12163/web:latest

heroku_release:
	heroku container:release web --app lit-citadel-12163

heroku_logs:
	heroku logs --app lit-citadel-12163

heroku_createdb:
	heroku run python manage.py recreate_db --app lit-citadel-12163

heroku_populatedb:
	heroku run python manage.py populate_db --app lit-citadel-12163

heroku_token:
	heroku auth:token

## app url https://lit-citadel-12163.herokuapp.com