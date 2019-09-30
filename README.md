To deploy: `git push heroku master`

Download Postgres:
https://postgresapp.com/downloads.html
Install CLI
https://postgresapp.com/documentation/cli-tools.html

Postgres migration: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

Initial run on heroku
To setup tables: 
1. heroku run python
2. from app import db
3. db.create_all()


## Running Postgres Locally
* start postgres server `psql postgres`
* connect to DB `\connect shipthatstinks`