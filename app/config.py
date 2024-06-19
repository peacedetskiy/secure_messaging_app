import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="../.env")

DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_SECRET = os.getenv('POSTGRES_SECRET')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
APP_SECRET = os.getenv('APP_SECRET')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_TOKEN_LOCATION = os.getenv('JWT_TOKEN_LOCATION')
