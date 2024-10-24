from celery import Celery
from os import getenv
import psycopg
import json
from psycopg.types.json import Json

REDIS_URI = getenv('REDIS_URI')
REDIS_BACKEND_DBINDEX = getenv('REDIS_BACKEND_DBINDEX')
REDIS_BROKER_DBINDEX = getenv('REDIS_BROKER_DBINDEX')
POSTGRES_URI = str(getenv('POSTGRES_URI'))

celery_app = Celery(main="saveres", broker=f"{REDIS_URI}/{REDIS_BROKER_DBINDEX}", backend=f"{REDIS_URI}/{REDIS_BACKEND_DBINDEX}")

@celery_app.task(ignore_result=True)
def save_res_to_db(url, ctx, content):
    db_conn = psycopg.connect(POSTGRES_URI)
    db_conn.set_autocommit(True)
    with db_conn.cursor() as cur:
        cur.execute("""INSERT INTO res (url, ctx, content) VALUES (%s, %s, %s);""", (url, Json(ctx), content))
    db_conn.close()

@celery_app.task(ignore_result=True)
def save_mro_to_db(url, domain, details):
    db_conn = psycopg.connect(POSTGRES_URI)
    db_conn.set_autocommit(True)
    with db_conn.cursor() as cur:
        cur.execute("""INSERT INTO mro (url, domain, details) VALUES (%s, %s, %s);""", (url, domain, Json(details)))
    db_conn.close()


@celery_app.task(ignore_result=True)
def save_err_to_db(url, ctx, error):
    db_conn = psycopg.connect(POSTGRES_URI)
    db_conn.set_autocommit(True)
    with db_conn.cursor() as cur:
        cur.execute("""INSERT INTO err (url, ctx, error) VALUES (%s, %s, %s);""", (url, Json(ctx), error))
    db_conn.close()