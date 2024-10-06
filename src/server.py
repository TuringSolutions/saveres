from fastapi import FastAPI, Response
from pydantic import BaseModel
from task import save_err_to_db, save_res_to_db
class ResData(BaseModel):
    url: str
    ctx: dict | str
    content : str

class ErrData(BaseModel):
    url: str
    ctx: dict | str
    error : str

app = FastAPI()

@app.post("/data")
async def save_data(res_data : ResData, response: Response):
    save_res_to_db.delay(url = res_data.url, ctx = res_data.ctx, content= res_data.content)
    response.status_code = 202
    return None

@app.post("/err")
async def save_err(err_data : ErrData, response: Response):
    save_err_to_db.delay(url = err_data.url, ctx = err_data.ctx, error= err_data.error)
    response.status_code = 202
    return None