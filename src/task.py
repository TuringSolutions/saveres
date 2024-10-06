from celery import Celery
from os import getenv
import psycopg
import json

REDIS_URI = getenv('REDIS_URI')
REDIS_BACKEND_DBINDEX = getenv('REDIS_BACKEND_DBINDEX')
REDIS_BROKER_DBINDEX = getenv('REDIS_BROKER_DBINDEX')
POSTGRES_URI = str(getenv('POSTGRES_URI'))

celery_app = Celery(main="saveres", broker=f"{REDIS_URI}/{REDIS_BROKER_DBINDEX}", backend=f"{REDIS_URI}/{REDIS_BACKEND_DBINDEX}")
db_conn = psycopg.connect(POSTGRES_URI)

@celery_app.task
def save_res_to_db(url, ctx, content):
    if isinstance(ctx, dict):
        ctx = json.dumps(ctx)
    cur = db_conn.cursor()
    cur.execute("""INSERT INTO res (url, ctx, content) VALUES (%s, %s, %s);""", (url, ctx, content))

@celery_app.task
def save_err_to_db(url, ctx, error):
    if isinstance(ctx, dict):
        ctx = json.dumps(ctx)
    cur = db_conn.cursor()
    cur.execute("""INSERT INTO err (url, ctx, error) VALUES (%s, %s, %s);""", (url, ctx, error))