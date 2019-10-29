To deploy: `git push heroku master`

Download Postgres:
https://postgresapp.com/downloads.html
Install CLI
https://postgresapp.com/documentation/cli-tools.html

Postgres migration: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

To connect to heroku postgres:
heroku pg:psql -a shipthatstinks-api-heroku

Initial run on heroku
To reset previous database:
1. heroku restart
2. heroku restart --confirm shipthatstinks-api-heroku

To setup tables remotely: 
1. heroku run python -a shipthatstinks-api-heroku
2. from app import db
3. db.create_all()

To setup tables locally: 
1. DROP DATABASE shipthatstinks;
2. CREATE DATABASE shipthatstinks;
3. flask db init
4. flask db migrate
5. flask db upgrade


Retry release:
heroku releases:retry --app shipthatstinks-api-heroku

Get local copy of remote database:
1. delete 
`heroku pg:pull DATABASE_URL ship-that-stinks-copy --app shipthatstinks-api-heroku`

Update sequences for autoincrement reset:
1. see sequences: `SELECT c.relname FROM pg_class c WHERE c.relkind = 'S';`
2. e.g. to update `SELECT setval('events_id_seq', (SELECT max(id) FROM events));`

## Running Postgres Locally
* start postgres server `psql postgres`
* connect to DB `\connect shipthatstinks`

Show tables `\dt`
* delete all rows from table: `TRUNCATE TABLE users CASCADE;`


Daily backups set with: heroku `pg:backups:schedule --at '04:00 Europe/London' --app shipthatstinks-api-heroku`