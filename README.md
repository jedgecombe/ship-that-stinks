## Setup
1. Copy `.env.example` into a new file called `.env` (ignored by git)
2. Enter values into `.env`
3. Download google cloud sdk following [these](https://cloud.google.com/sdk/docs/) instructions (and authenticate)

## To authenticate
* necessary each time, for local testing
1. `gcloud auth application-default login`
2. `gcloud sql instances describe ship-that-stinks` -> get connection name
3. `./cloud_sql_proxy -instances="the-ship-that-always-stinks:europe-west1:ship-that-stinks"=tcp:3306`