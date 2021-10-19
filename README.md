
## Usage

Build flask app, nginx and postresql. This will get the flask server and postgresql up and start the scheduler for the scrapper task once a day. Fill the secrets and configs in [.env](./.env) and [.env.db](./.env.db)

    docker-compose -f docker-compose.yml up -d --build


Initiate db with the app and create tables.

    docker-compose exec web python manage.py create_db


Populate the db with the first execution of the scrapper.

    docker-compose exec web python manage.py scrapper


To get the results from the scrapper:

    curl http://localhost/threats