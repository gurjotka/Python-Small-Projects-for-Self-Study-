from http.client import HTTPException

from fastapi import FastAPI, Request
import time
from logger import log_request

app = FastAPI()

@app.middleware("http")
async def request_logger(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)

        duration = time.time() - start_time

        log_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=duration
        )

        return response

    except Exception as e:
        duration = time.time() - start_time
        print(
            f"ERROR | {request.method} {request.url.path} |"
            f"{str(e)} | TIME={round(duration * 1000, 2)}ms"
        )
        raise e


@app.get("/hello")
def hello():
    return {"message": "Hello World, Konnichiwa!!"}


@app.get("/error")
def error():
    raise HTTPException(status_code=500, detail="Something went wrong")
