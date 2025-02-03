# monorepo
Backend Dev Case Study

## About the project
This is a backend case study with FastAPI, SQLAlchemy, Alembic, and PostgreSQL. This structure aims to maximize the code reusability and overcome the type incompatibility between the apps and the core.

## Running the project
To run this monorepo, you can install the python libraries used into your virtual environment, using <br>
`pip install -r requirements.txt`
<br><br>
After the installations are completed, please create a `.env` file and keep it under the main folder. Create a global variable for your database url, as <br>
`_DATABASE_URL="username:password@host/database_name"`<br>
The repository is configured to read and use this database url.
<br><br>
Because Alembic is individually scoped to apps, `cd` to each app in your venv and run `alembic upgrade head` on your console. In your, preferably, PSQL database three tables will be created: `alembic_version_app1`, `alembic_version_app2`, and `ledger entries`.<br><br>
To run the apps, `cd` to where their individual `main.py` files are and run on your console `uvicorn app1_main:app --port 8000` and `uvicorn app2_main:app --port 8001`.

## Some points
### Enum in Subclasses
My approach was to create a metaclass, in which the `cls` was compared to a list of four required operation names. If any of them was missing, it raises a `TypeError` demanding the missing operation must be included. With this metaclass, the required operations can be easily inherited to the subclasses without having to inherit any enums.
### Individually scoped Alembics
Because alembic tends to drop a table if it already exists, I had to exclude other `alembic_version` tables. This way, we can keep track of the alembic versions of each application. <br>
`excluded_tables = {"alembic_version_app1", "alembic_version_app2"} - {current_version_table}` line also allows for the easy addition and removal of new applications. For better and future use, the list of version tables may be moved to `.env`. This way, the list will remain global and private.
### Enums in the Database
Because each application is assumed to have individual operations, having them all enumerated in the database from the beginning would not be feasible. Storing a yet-to-be-used application's operations would be necessary. Instead, my approach was to first enumerate the four core operations in the database. Later, every application gets to alter the enumeration in `pg_type` according to their own operations as they are used.
