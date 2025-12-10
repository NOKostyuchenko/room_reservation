# Meeting room booking service

## Creating and activating a virtual environment
`python -m venv venv`
`venv/Scripts/activate`

## Installing packages
`pip install -r requirements.txt`

## Project launch
`python app/main.py`

## Environment variables

### Configuring the FastAPI app

|  Variable name |      Description     |  Example  |  The standard value  |
|----------------|----------------------|-----------|----------------------|
|    APP_HOST    | Host for the FastAPI | '0.0.0.0' |      'localhost'     |
|    APP_PORT    | Port for the FastAPI |    8000   |          8080        |

### DB configuration

|  Variable name |      Description     |  Example  |
|----------------|----------------------|-----------|
|     DB_USER    | User name for the DB |   'user'  |    
|   DB_PASSWORD  |  Password for the DB |   '123'   |
|     DB_HOST    |   Host for the DB    |'127.0.0.1'|
|     DB_PORT    |   Port for the DB    |    8000   |
|     DB_NAME    |    Database name     |    8000   |  

### Migration SQLite
`alembic upgrade head`