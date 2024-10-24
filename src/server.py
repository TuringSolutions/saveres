from fastapi import FastAPI, Response
from pydantic import BaseModel
from task import save_err_to_db, save_res_to_db, save_mro_to_db
from typing import Any

class ResData(BaseModel):
    url: str
    ctx: dict
    content : Any

class ErrData(BaseModel):
    url: str
    ctx: dict
    error : str

class MROData(BaseModel):
    url : str
    domain: str
    details: dict

app = FastAPI()

@app.post("/res")
async def save_data(res_data : ResData, response: Response):
    save_res_to_db.delay(url = res_data.url, ctx = res_data.ctx, content= res_data.content)
    response.status_code = 202
    return None

@app.post("/err")
async def save_err(err_data : ErrData, response: Response):
    save_err_to_db.delay(url = err_data.url, ctx = err_data.ctx, error= err_data.error)
    response.status_code = 202
    return None

@app.post("/mro")
async def save_mro(res_data: MROData, response: Response):
    save_mro_to_db.delay(url = res_data.url, domain = res_data.domain, details=res_data.details)
    response.status_code = 202
    return None

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/mirror")
async def mirror(body: ResData):
    print(f"Body is : {body}")
    return None