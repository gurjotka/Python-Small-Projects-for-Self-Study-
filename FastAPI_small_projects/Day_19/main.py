from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import time


app = FastAPI()

requests_store = {}


@app.middleware("http")
async def rate_limiter(request: Request, call_next):

    client_ip = request.client.host
    current_time = time.time()

    window_seconds = 60
    max_requests = 5

    if client_ip not in requests_store:
        requests_store[client_ip] = []

    requests_store[client_ip] = [
        timestamp
        for timestamp in requests_store[client_ip]
        if current_time - timestamp < window_seconds
    ]

    if len(requests_store[client_ip]) >= max_requests:

        return JSONResponse(
            status_code= 429,
            content={
                "error": "Too many requests. Ty again later."
            }
        )

    requests_store[client_ip].append(current_time)

    response = await call_next(request)
    return response


@app.get("/")
def home():
    return {
        "message": "Welcome"
    }