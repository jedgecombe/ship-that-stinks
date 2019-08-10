import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = "secret"
DATA_BACKEND = "cloudsql"

# google Cloud Project ID
PROJECT_ID = "the-ship-that-always-stinks"

# CloudSQL & SQLAlchemy config
CLOUDSQL_USER = os.environ.get("MYSQL_USER")
CLOUDSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
CLOUDSQL_DATABASE = "ship_that_stinks"
# Set this value to the Cloud SQL connection name, e.g.
#   "project:region:cloudsql-instance".
# You must also update the value in app.yaml.
CLOUDSQL_CONNECTION_NAME = "the-ship-that-always-stinks:europe-west1:ship-that-stinks"

LOCAL_SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}"
).format(user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD, database=CLOUDSQL_DATABASE)

LIVE_SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://{user}:{password}@localhost/{database}"
    "?unix_socket=/cloudsql/{connection_name}"
).format(
    user=CLOUDSQL_USER,
    password=CLOUDSQL_PASSWORD,
    database=CLOUDSQL_DATABASE,
    connection_name=CLOUDSQL_CONNECTION_NAME,
)

if os.environ.get("GAE_INSTANCE"):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
