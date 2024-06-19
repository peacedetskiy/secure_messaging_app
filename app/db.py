from psycopg2 import connect
from flask import g
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_db():
    if 'db' not in g:
        db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        g.db = connect(db_url)
    return g.db
