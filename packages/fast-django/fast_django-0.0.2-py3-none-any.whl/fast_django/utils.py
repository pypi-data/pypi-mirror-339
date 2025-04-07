import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

load_dotenv()


class DbBackend:
    SQLITE3 = "django.db.backends.sqlite3"
    POSTGRESQL = "django.db.backends.postgresql"
    MYSQL = "django.db.backends.mysql"


def create_db(db_backend: str = DbBackend.POSTGRESQL):
    if db_backend == DbBackend.POSTGRESQL:
        conn = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
            [os.getenv("DB_NAME")],
        )
        exists = cur.fetchone()
        if not exists:
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(os.getenv("DB_NAME"))  # type: ignore
                )
            )
        cur.close()
        conn.close()
    else:
        raise ValueError(f"Database type {db_backend} not supported")
