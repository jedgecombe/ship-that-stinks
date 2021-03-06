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
4. flask db stamp heads  (if target database not up to date)
4. flask db migrate
5. flask db upgrade

To migrate remote:
- download remote db
- run db migrate (and maybe stamp heads)
- run db upgrade

TODO NEXT - seems to be messed up with migrations. Delete history and start again.
Retry release:
heroku releases:retry --app shipthatstinks-api-heroku

Get local copy of remote database:
1. `DROP DATABASE "ship-that-stinks-staging";`
2. `heroku pg:pull DATABASE_URL ship-that-stinks-staging --app shipthatstinks-api-heroku`
THEN run migrations (delete migrations/ and table alembic_version if necessary)
i.e. flask db init / flask db migrate / flask db upgrade
THEN push to remote
`heroku run flask db upgrade -a shipthatstinks-api-heroku`

Update sequences for autoincrement reset:
1. see sequences: `SELECT c.relname FROM pg_class c WHERE c.relkind = 'S';`
2. e.g. to update `SELECT setval('events_id_seq', (SELECT max(id) FROM events));`

## Running Postgres Locally
* start postgres server `psql postgres`
* connect to DB `\connect shipthatstinks`

Show tables `\dt`
* delete all rows from table: `TRUNCATE TABLE users CASCADE;`


Daily backups set with: heroku `pg:backups:schedule --at '04:00 Europe/London' --app shipthatstinks-api-heroku`

To reset password
1. `heroku run python -a shipthatstinks-api-heroku`
from app import db
from app.models import User
user = User.query.filter_by(id=5).first()
user.set_password(form.password.data)
db.session.add(user)
db.session.commit()